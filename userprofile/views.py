from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from payment.models import ShippingAddress
from .models import Profile
from payment.models import Order
from .forms import ProfilePartialForm, ShippingAddressForm
from django.urls import reverse

@login_required
def initialize_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfilePartialForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile details have been updated successfully.")
            return redirect('profile')
    else:
        form = ProfilePartialForm(instance=profile)

    return render(request, 'initialize-profile.html', {'form': form})


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    shipping_addresses = ShippingAddress.objects.filter(user=request.user).order_by('-is_default', 'id')  
 
    # Filter orders by status
    pending_orders = Order.objects.filter(user=request.user, status='Pending')
    completed_orders = Order.objects.filter(user=request.user, status='Complete')
    cancelled_orders = Order.objects.filter(user=request.user, status='Cancel')

    return render(request, 'profile.html', {
        'profile': profile,
        'shipping_addresses': shipping_addresses,
        'add_form': ShippingAddressForm(),
        'edit_forms': {address.id: ShippingAddressForm(instance=address) for address in shipping_addresses},
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'cancelled_orders': cancelled_orders,
    })

@login_required
def add_shipping_address(request):
    if request.method == 'POST':
        add_form = ShippingAddressForm(request.POST)
        if add_form.is_valid():
            new_address = add_form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            messages.success(request, "New shipping address added successfully.")
            return HttpResponseRedirect(reverse('profile') + '#shipping-address-manage')
    else:
        messages.error(request, "Failed to add shipping address.")

    return HttpResponseRedirect(reverse('profile') + '#shipping-address-manage')

@login_required
def set_default_address(request):
    address = get_object_or_404(ShippingAddress, id=request.POST.get('address_id'), user=request.user)
    if address:
        ShippingAddress.objects.filter(user=request.user).update(is_default=False)
        address.is_default = True
        address.save()
        messages.success(request, "Default shipping address updated successfully.")
    else:
        messages.error(request, "Failed to update default shipping address.")

    return HttpResponseRedirect(reverse('profile') + '#shipping-address-manage')

@login_required
def edit_shipping_address(request, address_id):
    address = get_object_or_404(ShippingAddress, id=address_id, user=request.user)
    
    if request.method == 'POST':
        edit_form = ShippingAddressForm(request.POST, instance=address)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, "Shipping address updated successfully.")
            return HttpResponseRedirect(reverse('profile') + '#shipping-address-manage')
    else:
        messages.error(request, "Failed to update shipping address.")

    return HttpResponseRedirect(reverse('profile') + '#shipping-address-manage')

@login_required
def delete_address(request, address_id):
    address = get_object_or_404(ShippingAddress, id=address_id, user=request.user)
    if request.method == 'POST':
        address.delete()
        messages.success(request, "Shipping address deleted successfully.")
        return HttpResponseRedirect(reverse('profile') + '#shipping-address-manage')
    else:
        messages.error(request, "Failed to delete shipping address.")

    return HttpResponseRedirect(reverse('profile') + '#shipping-address-manage')

@login_required  
def update_user_info(request):
    if request.method == 'POST' and request.POST.get('action') == 'update_info':
        try:
            username = request.POST.get('username', '').strip()
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            address1 = request.POST.get('address1', '').strip()
            address2 = request.POST.get('address2', '').strip()
            city_province = request.POST.get('city_province', '').strip()
            district = request.POST.get('district', '').strip()

            if not username or not first_name or not last_name or not email:
                return JsonResponse({'success': False, 'error': 'All fields are required.'})

            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                return JsonResponse({'success': False, 'error': 'Email is already in use by another user.'})

            # Update user fields
            user = request.user
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

            # Update profile fields
            profile, created = Profile.objects.get_or_create(user=user)
            profile.phone = phone
            profile.address1 = address1
            profile.address2 = address2
            profile.city_province = city_province
            profile.district = district
            profile.save()

            return JsonResponse({'success': True, 'message': 'User information updated successfully.'})
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request: only POST and AJAX requests are allowed.'})

def delete_address(request, address_id):
    if request.method == "POST":
        address = get_object_or_404(ShippingAddress, id=address_id)
        address.delete()
        return redirect('profile')

@login_required
def update_user_password(request):
    if request.method == 'POST' and request.POST.get('action') == 'update_password':
        try:
            print(f"POST data: {request.POST}")

            new_password = request.POST.get('new_password', '').strip()
            confirm_password = request.POST.get('confirm_password', '').strip()

            print(f"New Password: {new_password}, Confirm Password: {confirm_password}")

            if not new_password or not confirm_password:
                return JsonResponse({'success': False, 'error': 'All password fields are required.'})

            user = request.user

            if new_password != confirm_password:
                return JsonResponse({'success': False, 'error': 'New password and confirmation password do not match.'})

            user.set_password(new_password)
            user.save()

            update_session_auth_hash(request, user)
            messages.success(request, 'Password updated successfully.')
            return JsonResponse({'success': True, 'message': 'Password updated successfully.'})
        
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        messages.error(request, 'Invalid request method.')
        return JsonResponse({'success': False, 'error': 'Invalid request: only POST and AJAX requests are allowed.'})
