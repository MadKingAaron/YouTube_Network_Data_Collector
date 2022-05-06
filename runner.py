import video_viewer, loadVideoList

def main():
    video_list = loadVideoList.loadVideoList('youtubeVideoList.txt')
    for video in video_list:
        viewer = video_viewer.YouTube_Viewer(video_url=video)
        viewer.start_video()
        viewer.stop_session()

if __name__ == '__main__':
    main()
