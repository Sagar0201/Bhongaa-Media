from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage

# Create your views here.
from django.http import request
from django.shortcuts import render, HttpResponse, redirect
# from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Posts
from .models import ContactInfo


def home(request):
    posts =[]
    index=0
    for i in Posts.objects.all():
        if index==5:
            break
        else:
            posts.append(i)
            index+=1

    
    return render(request, 'index.html', {'posts': posts})


def Login(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return redirect("home")
            else:
                messages.error(request, "You're Account is Disable")
        else:
            messages.error(
                request, "Invalid Username Or Password please try again")
            return redirect('/Login', {"loginusername": loginusername, "loginpassword": loginpassword})

    return render(request, 'Accounts/Login.html')


@login_required(login_url="/Login/")
def SignOut(request):
    auth.logout(request)
    messages.success(request, "Successfully logged out")
    return redirect("/")


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_subject = request.POST.get('message_subject')
        message = request.POST.get('message')
        Contact_us = ContactInfo(
            name=name, email_address=email, message_subject=message_subject, message=message)
        Contact_us.save()
        messages.success(request, "Message Send  Successfully")
    return render(request, 'Bhongaa/Contact.html')


def about(request):
    return render(request, 'Bhongaa/AboutUs.html')


def search(request):
    search = request.GET.get('Query')
    page_num = request.GET.get('page')
    PostCategory = request.GET.get('PostCategory')
    PostCategorys={"All","Image","Video"}
    for i in Posts.objects.all():
        PostCategorys.add(i.Category)

    if len(search) > 78:
        posts = Posts.objects.none()
    else:

        title = Posts.objects.filter(
            Title__icontains=search)
        Category = Posts.objects.filter(
            Category__icontains=search)
        description = Posts.objects.filter(
            Description__icontains=search)
        timestamp = Posts.objects.filter(
            timestamp__icontains=search)

        posts = (title | description | timestamp | Category ).distinct()

        if PostCategory is None:
            posts = posts
            PostCategory = "All"
        else:
            print(PostCategory)
            if PostCategory == "All":
                posts = posts
                PostCategory = PostCategory

            elif PostCategory == "Image":
                bhongaa_posts = posts
                posts= []
                for i in bhongaa_posts:
                    if i.file_type == "Image":
                        posts.append(i)
                PostCategory = PostCategory

            elif PostCategory == "Video":
                bhongaa_posts = posts
                posts= []
                for i in bhongaa_posts:
                    if i.file_type == "Video":
                        posts.append(i)
                PostCategory = PostCategory
            else:
                bhongaa_posts = posts
                posts= []
                for i in bhongaa_posts:
                    if i.Category == PostCategory:
                        posts.append(i)
                PostCategory = PostCategory

        if page_num is None:
            page_num = 1
        p = Paginator(posts, 8)
        try:
            posts = p.page(page_num)
        except EmptyPage:
            posts = p.page(p.num_pages)

        if len(posts) == 0:
            messages.warning(
                request, "No Search results Found. Please refine your query. Please Try Another KeyWords.")
    return render(request, 'Bhongaa/Search.html', {"Query": search, "posts": posts, "PostCategory": PostCategory,"PostCategorys":PostCategorys})


def allposts(request):
    PostCategory = request.GET.get('PostCategory')
    page_num = request.GET.get('page')
    PostCategorys={"All","Image","Video"}
    for i in Posts.objects.all():
        PostCategorys.add(i.Category)

    if PostCategory is None:
        posts = Posts.objects.all()
        PostCategory = "All"

    else:
        print(PostCategory)
        if PostCategory == "All":
            posts = Posts.objects.all()
            PostCategory = PostCategory

        elif PostCategory == "Image":
            posts = Posts.objects.filter(file_type=PostCategory)
            PostCategory = PostCategory

        elif PostCategory == "Video":
            posts = Posts.objects.filter(file_type=PostCategory)
            PostCategory = PostCategory
        else:
            posts= Posts.objects.filter(Category=PostCategory)
            PostCategory = PostCategory
            

    if page_num is None:
        page_num = 1
    p = Paginator(posts,8)
    try:
        bhongaa_posts = p.page(page_num)
    except EmptyPage:
        bhongaa_posts = p.page(p.num_pages)
    return render(request, 'Bhongaa/AllPosts.html', {'posts': bhongaa_posts, "PostCategory": PostCategory,"PostCategorys":PostCategorys})


def post(request):
    post_id = request.GET.get('post')
    posts = Posts.objects.filter(id=post_id)
    return render(request, 'Bhongaa/Post.html', {'posts': posts})


def addpost(request):
    if request.method == 'POST':
        file = request.FILES['file']
        Title = request.POST.get('Title')
        Category = request.POST.get('Category')
        Category=Category.capitalize()
        print(Category)
        Description = request.POST.get('Description')
        print(file, Title, Description)
        str1 = str(file.name)
        if str1.endswith((".jpg", ".png", ".gif")):
            file_type = "Image"
        if str1.endswith((".mp4", ".3gp", ".ogg")):
            file_type = "Video"
        posts = Posts(
            file=file, file_type=file_type, Title=Title,Category=Category ,Description=Description)
        posts.save()
        messages.success(request, "Posts Created  Successfully")
    return render(request, 'Bhongaa/AddPosts.html')


@login_required(login_url="/Login/")
def Profile(request):
    if request.method == "POST":
        PostId = request.POST.get('PostId')
        if PostId is not None:
            PostsDelete = Posts.objects.get(pk=PostId)
            PostsDelete.delete()
            messages.success(request, "Post Delete Sucessfully")
            return redirect("Profile")
        return redirect("/Profile")
    posts = Posts.objects.all()
    no_posts = len(posts)
    return render(request, 'Accounts/Profile.html', {"posts": posts, "no_posts": no_posts})


@login_required(login_url="/home/")
def Messages(request):
    Query = request.GET.get('Query')
    if request.method == "POST":
        message_id = request.POST.get('message_id')
        contact_message = ContactInfo.objects.all()
        sender_message = ContactInfo.objects.filter(id=message_id)
        return render(request, 'Accounts/Messages.html', {"contact_message": contact_message, "sender_message": sender_message})
    if Query is None:
        contact_message = ContactInfo.objects.all()
    else:
        name = ContactInfo.objects.filter(
            name__icontains=Query)
        email_address = ContactInfo.objects.filter(
            email_address__icontains=Query)
        contact_message = name.union(email_address)
    return render(request, 'Accounts/Messages.html', {"contact_message": contact_message})

def OurClient(request):
    return render(request, 'Bhongaa/OurClient.html')