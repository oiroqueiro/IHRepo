from .forms import EditVideoForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Videos, Subtitles, Summaries, Keywords
from .IHRepo import filter_videos, video_player

# Create your views here.

# this is a view for listing all the videos
def home(request):
    #filtering
    searching_filter = request.GET.get('search')
    
    # retrieving all the videos from the database    
    if searching_filter != '' and searching_filter is not None:        
        #videos = Videos.objects.filter(video_name__icontains=searching_filter).values()
        videos = Videos.objects.filter(id__in=filter_videos(searching_filter)).values()
    else:
        videos = Videos.objects.all()        
    context = {'videos': videos}
  
    return render(request, 'ihrepo/home.html', context)

# this is a view for listing a single video
def video_detail(request, id):
    # querying a particular book by its id
    video = Videos.objects.get(pk=id)
    context = {'video': video}
    return render(request, 'ihrepo/video-detail.html', context)

# this is a view for adding a video
def add_video(request):
    # checking if the method is POST
    if request.method == 'POST':
        # getting all the data from the POST request
        data = request.POST
        # getting the image
        #image = request.FILES.get('image-file')
        # creating and saving the video
        video = Videos.objects.create(
           video_name = data['video_name'],
           video_path = data['video_path']
        )
        #DO ALL THE LOGIC
        # going to the home page
        return redirect('home')
    return render(request, 'ihrepo/add-video.html')

# this is a view for editing the video's info
def edit_video(request, id):
    # getting the video to be updated
    video = Videos.objects.get(pk=id)
    # populating the form with the video's information
    form = EditVideoForm(instance=video)
    # checking if the request is POST
    if request.method == 'POST':
        # filling the form with all the request data 
        form = EditVideoForm(request.POST, request.FILES, instance=video)
        # checking if the form's data is valid
        if form.is_valid():
            # saving the data to the database
            form.save()
            # redirecting to the home page
            return redirect('home')
    context = {'form': form}
    return render(request, 'ihrepo/update-video.html', context)

# this is a view for deleting a video
def delete_video(request, id):
    # getting the video to be deleted
    video = Videos.objects.get(pk=id)
    # checking if the method is POST
    if request.method == 'POST':
        # delete the video
        video.delete()
        # return to home after a success delete
        return redirect('home')
    context = {'video': video}
    return render(request, 'ihrepo/delete-video.html', context)

# this is a view for deleting a book
def play_video(request, id, langid):
    # getting the video to be play
    video = Videos.objects.get(pk=id)
    # checking if the method is POST
    print(request)
    print(id)
    print(langid)
    if request.method == 'GET':
        # play the video
        #return HttpResponse(video_player(video.id, langid))
        video_player(video.id,langid)    
        # return to home after a success play
        return redirect('home')
    context = {'video': video}
    return render(request, 'ihrepo/play-video.html', context)