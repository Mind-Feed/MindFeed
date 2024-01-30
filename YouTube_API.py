import tkinter as tk
from tkinter import ttk
import googleapiclient.discovery
import webbrowser

def run_youtube_search_app():
    # Replace 'YOUR_API_KEY' with the actual API key you obtained
    API_KEY = 'AIzaSyCJrBa4FuRoZ7j4rOiPS5VRPHEQPK7NLHQ'

    def search_videos(query, max_results=5):
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

        request = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            maxResults=max_results
        )

        response = request.execute()
        videos = response['items']

        video_info_list = []
        for video in videos:
            video_id = video['id']['videoId']
            video_info = get_video_info(video_id)
            video_info_list.append(video_info)

        return video_info_list

    def get_video_info(video_id):
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

        request = youtube.videos().list(
            part="snippet",
            id=video_id
        )

        response = request.execute()
        video_info = response['items'][0]

        return video_info

    def open_video_link(event):
        widget = event.widget
        index = widget.index(tk.CURRENT)
        link_start = widget.search(" [Link](", index, backwards=True, regexp=True)

        if link_start:
            link_start = widget.index(link_start)
            link_end = widget.search(")", index, regexp=True)
            if link_end:
                link_end = widget.index(link_end)
                link = widget.get(link_start + 8, link_end)
                webbrowser.open(link)

    def search_and_display():
        query = entry_query.get()
        max_results = 5

        videos = search_videos(query, max_results)

        result_text.delete(1.0, tk.END)  # Clear previous results

        for i, video_info in enumerate(videos, start=1):
            title = video_info['snippet']['title']
            video_id = video_info['id']
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            result_text.insert(tk.END, f"{i}. {title}\n")
            result_text.insert(tk.END, f"   [Link]({video_url})\n\n")

        result_text.tag_configure("hyperlink", foreground="blue", underline=True)
        result_text.tag_add("hyperlink", "1.0", tk.END)
        result_text.bind("<Button-1>", open_video_link)

    # Create the main application window
    app = tk.Tk()
    app.title("YouTube API Search")

    # Set the size of the window
    app.geometry("800x600")  # Width x Height

    # Configure a ttk style
    style = ttk.Style()
    style.configure("TButton", padding=(10, 5, 10, 5), font=('arial', 12))
    style.configure("TLabel", padding=(10, 5, 10, 5), font=('arial', 12))
    style.configure("TEntry", padding=(10, 5, 10, 5), font=('arial', 12))
    style.configure("TText", padding=(10, 5, 10, 5), font=('arial', 12))

    # Create and place the widgets with ttk styling
    label_query = ttk.Label(app, text="Enter search query:")
    label_query.pack(pady=10)

    entry_query = ttk.Entry(app)
    entry_query.pack(pady=10)

    search_button = ttk.Button(app, text="Search", command=search_and_display)
    search_button.pack(pady=10)

    result_text = tk.Text(app, height=40, width=100)
    result_text.pack(pady=10)

    # Start the Tkinter event loop
    app.mainloop()

# Run the application
run_youtube_search_app()
