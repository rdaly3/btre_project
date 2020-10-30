from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail
from .models import Contact


def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # Check if user has made inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(
                listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(
                    request, 'You have already have an active inquiry for this listing')
                return redirect('/listings/'+listing_id)

        contact = Contact(listing=listing, listing_id=listing_id, name=name,
                          email=email, phone=phone, message=message, user_id=user_id)

        contact.save()

        # Send Email
        send_mail(
            'You\'ve got a new Property Inquiry!',
            'A user has submitted an inquiry about one of your properties! Someone is curious about ' +
            listing + '. Sign into the admin panel for more info.',
            'desertcitysoundtrack@gmail.com',
            [realtor_email, 'rscottdaly@gmail.com'],
            fail_silently=False,
        )

        messages.success(
            request, 'Your request has been submitted, a Realtor will get in touch with you soon.')

        return redirect('/listings/'+listing_id)
