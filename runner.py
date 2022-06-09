import video_viewer, loadVideoList
import sys

def main():
    #if len(sys.argv) < 2:
    #    print('Make sure to add linux password as cmd argument')
    #else:

    repeat=True

    video_list = loadVideoList.loadVideoList('youtubeVideoList_10.txt')
    while(True):
        for video in video_list:
            try:
                viewer = video_viewer.YouTube_Viewer(video_url=video, headless=True)
                viewer.start_video()
                viewer.stop_session()
            except:
                pass
        if(not repeat):
            break

if __name__ == '__main__':
    main()
