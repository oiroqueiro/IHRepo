from .forms import EditVideoForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Videos, Subtitles, Summaries, Keywords
from .IHRepo import filter_videos, video_player, search_pos_video


# Create your views here.

# this is a view for listing all the videos
def home(request):
    #filtering
    searching_filter = request.GET.get('search')
    
    # retrieving all the videos from the database    
    if searching_filter != '' and searching_filter is not None:                
        #videos = Videos.objects.filter(id__in=filter_videos(searching_filter)).values()        
        videos = Videos.objects.filter(id__in=filter_videos(searching_filter)).prefetch_related('keywords_set', 'summaries_set', 'subtitles_set')      
    else:
        videos = Videos.objects.all().prefetch_related('keywords_set', 'summaries_set', 'subtitles_set')       

    context = {'videos': videos}
  
    return render(request, 'ihrepo/home.html', context)

# this is a view for listing a single video
def video_detail(request, id):
    # querying a particular book by its id
    video = Videos.objects.get(pk=id)

    search_in_filter = request.GET.get('search_in')
    langid_filter = request.GET.get('langid')
        

    # get the subtitles in the selected language
    subtitles = Subtitles.objects.filter(videoid=id, languageid=langid_filter).first()


    # search for the text in the subtitles if search_in_filter is not empty
    positions = []
    if search_in_filter and subtitles:
        positions = search_pos_video(subtitles.subtitles, search_in_filter)

    context = {'video': video, 'positions': positions, 'search_in': search_in_filter}
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

# this is a view for playing a video
def play_video(request, id, langid, position):
    # getting the video to be play
    video = Videos.objects.get(pk=id)

    # checking if the method is POST
    if request.method == 'GET':
        # play the video
        #return HttpResponse(video_player(video.id, languageid))
        video_player(video.id,langid,position)    
        # return to home after a success play
        return redirect('home')
    context = {'video': video}
    return render(request, 'ihrepo/play-video.html', context)


# function to show details 

def get_summary(request, id):
    video = get_object_or_404(Videos, id=id)
    langid = request.GET.get("langid", "en")
    summary = Summaries.objects.filter(video=video, languageid=langid).first()
    if summary:
        return JsonResponse({"summary": summary.summary})
    else:
        return JsonResponse({"summary": ""})