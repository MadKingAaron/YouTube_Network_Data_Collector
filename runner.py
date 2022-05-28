import video_viewer, loadVideoList
import sys

def main():
    if len(sys.argv) < 2:
        print('Make sure to add linux password as cmd argument')
    else:
        video_list = loadVideoList.loadVideoList('youtubeVideoList.txt')
        for video in video_list:
            for i in range(5):
                print(i, video)
                try:
                    viewer = video_viewer.YouTube_Viewer(video_url=video, headless=True)
                    viewer.start_video(password=sys.argv[1])
                    viewer.stop_session()
                    del viewer
                except:
                    print("Skip")
                    pass

if __name__ == '__main__':
    main()
