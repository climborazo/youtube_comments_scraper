#!/usr/bin/env python3

import os
import json
import csv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
import re

YOUTUBE_API_KEY = "****************************************"

class YouTubeCommentsScraper:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        
    def get_channel_id(self, channel_username: str = None, channel_url: str = None, channel_handle: str = None) -> Optional[str]:
        try:
            if channel_handle:
                channel_handle = channel_handle.lstrip('@')
                try:
                    request = self.youtube.search().list(
                        part='snippet',
                        q=channel_handle,
                        type='channel',
                        maxResults=1
                    )
                    response = request.execute()
                    if response['items']:
                        return response['items'][0]['snippet']['channelId']
                except:
                    pass
                
                channel_username = channel_handle
            
            if channel_username:
                try:
                    request = self.youtube.channels().list(
                        part='id',
                        forUsername=channel_username
                    )
                    response = request.execute()
                    
                    if response['items']:
                        return response['items'][0]['id']
                except:
                    pass
                
                request = self.youtube.search().list(
                    part='snippet',
                    q=channel_username,
                    type='channel',
                    maxResults=1
                )
                response = request.execute()
                
                if response['items']:
                    return response['items'][0]['snippet']['channelId']
            
            if channel_url:
                if '@' in channel_url:
                    username = channel_url.split('@')[1].split('/')[0]
                    return self.get_channel_id(channel_handle=username)
                elif '/channel/' in channel_url:
                    return channel_url.split('/channel/')[1].split('/')[0].split('?')[0]
                elif '/c/' in channel_url:
                    username = channel_url.split('/c/')[1].split('/')[0]
                    return self.get_channel_id(channel_username=username)
                    
        except HttpError as e:
            print(f"Error Getting Channel ID: {e}")
        
        return None
    
    def get_channel_info(self, channel_id: str) -> Dict:
        try:
            request = self.youtube.channels().list(
                part='snippet',
                id=channel_id
            )
            response = request.execute()
            
            if response['items']:
                snippet = response['items'][0]['snippet']
                return {
                    'title': snippet['title'],
                    'description': snippet.get('description', ''),
                    'custom_url': snippet.get('customUrl', '')
                }
        except HttpError as e:
            print(f"Error Getting Channel Info: {e}")
        
        return {'title': 'Unknown_Channel', 'description': '', 'custom_url': ''}
    
    def sanitize_filename(self, filename: str) -> str:
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        filename = filename.replace(' ', '_')
        filename = filename.lower()
        if len(filename) > 100:
            filename = filename[:100]
        return filename
    
    def get_channel_videos(self, channel_id: str) -> List[Dict]:
        videos = []
        
        try:
            request = self.youtube.channels().list(
                part='contentDetails',
                id=channel_id
            )
            response = request.execute()
            
            if not response['items']:
                print("Channel Not Found")
                return videos
            
            uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            next_page_token = None
            
            while True:
                request = self.youtube.playlistItems().list(
                    part='snippet',
                    playlistId=uploads_playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                )
                response = request.execute()
                
                for item in response['items']:
                    video_info = {
                        'video_id': item['snippet']['resourceId']['videoId'],
                        'title': item['snippet']['title'],
                        'published_at': item['snippet']['publishedAt']
                    }
                    videos.append(video_info)
                    print(f"Found Video: {video_info['title']}")
                
                next_page_token = response.get('nextPageToken')
                
                if not next_page_token:
                    break
            
            print(f"\nTotal Videos Found: {len(videos)}")
            
        except HttpError as e:
            print(f"Error Getting Videos: {e}")
        
        return videos
    
    def get_video_comments(self, video_id: str) -> List[Dict]:
        comments = []
        
        try:
            next_page_token = None
            
            while True:
                request = self.youtube.commentThreads().list(
                    part='snippet,replies',
                    videoId=video_id,
                    maxResults=100,
                    pageToken=next_page_token,
                    textFormat='plainText'
                )
                response = request.execute()
                
                for item in response['items']:
                    top_comment = item['snippet']['topLevelComment']['snippet']
                    
                    comment_data = {
                        'video_id': video_id,
                        'comment_id': item['snippet']['topLevelComment']['id'],
                        'author': top_comment['authorDisplayName'],
                        'author_channel_id': top_comment.get('authorChannelId', {}).get('value', ''),
                        'text': top_comment['textDisplay'],
                        'like_count': top_comment['likeCount'],
                        'published_at': top_comment['publishedAt'],
                        'updated_at': top_comment['updatedAt'],
                        'is_reply': False,
                        'parent_id': None
                    }
                    comments.append(comment_data)
                    
                    if 'replies' in item:
                        for reply in item['replies']['comments']:
                            reply_snippet = reply['snippet']
                            
                            reply_data = {
                                'video_id': video_id,
                                'comment_id': reply['id'],
                                'author': reply_snippet['authorDisplayName'],
                                'author_channel_id': reply_snippet.get('authorChannelId', {}).get('value', ''),
                                'text': reply_snippet['textDisplay'],
                                'like_count': reply_snippet['likeCount'],
                                'published_at': reply_snippet['publishedAt'],
                                'updated_at': reply_snippet['updatedAt'],
                                'is_reply': True,
                                'parent_id': item['snippet']['topLevelComment']['id']
                            }
                            comments.append(reply_data)
                
                next_page_token = response.get('nextPageToken')
                
                if not next_page_token:
                    break
            
        except HttpError as e:
            if e.resp.status == 403:
                print(f"Comments Disabled For Video {video_id}")
            else:
                print(f"Error Getting Comments For {video_id}: {e}")
        
        return comments
    
    def scrape_channel_comments(self, channel_id: str) -> tuple:
        all_comments = []
        
        channel_info = self.get_channel_info(channel_id)
        channel_name = channel_info['title']
        
        print(f"\nChannel Name: {channel_name}")
        print("="*60)
        
        videos = self.get_channel_videos(channel_id)
        
        if not videos:
            print("No Videos Found")
            return all_comments, channel_name
        
        for idx, video in enumerate(videos, 1):
            print(f"\n[{idx}/{len(videos)}] Downloading Comments For: {video['title']}")
            
            comments = self.get_video_comments(video['video_id'])
            
            for comment in comments:
                comment['video_title'] = video['title']
                comment['video_published_at'] = video['published_at']
                comment['channel_name'] = channel_name
            
            all_comments.extend(comments)
            print(f"  -> {len(comments)} Comments Found")
        
        print("\n")
        print(f"Total Comments Downloaded: {len(all_comments)}")
        
        return all_comments, channel_name
    
    def save_reports(self, comments: List[Dict], channel_name: str):
        if not comments:
            print("No Comments To Save")
            return
        
        reports_dir = Path('reports')
        reports_dir.mkdir(exist_ok=True)
        
        safe_channel_name = self.sanitize_filename(channel_name)
        channel_dir = reports_dir / safe_channel_name
        channel_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        json_file = channel_dir / f'youtube_comments_{timestamp}.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(comments, f, ensure_ascii=False, indent=2)
        print(f"\n✅ Json Saved: {json_file}")
        
        csv_file = channel_dir / f'youtube_comments_{timestamp}.csv'
        if comments:
            keys = comments[0].keys()
            with open(csv_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(comments)
        print(f"✅ Csv Saved: {csv_file}")
        
        try:
            from html_report_generator import generate_html_report
            html_file = channel_dir / f'youtube_comments_report_{timestamp}.html'
            generate_html_report(str(json_file), str(html_file))
        except ImportError:
            print("⚠️ Html Report Generator Not Found - Skipping Html Generation")
        except Exception as e:
            print(f"⚠️ Error Generating Html Report: {e}")
        return str(json_file)


def main():
    print ("\n")
    print("Youtube Comments Scraper")
    
    if YOUTUBE_API_KEY == "YOUR_API_KEY_HERE" or not YOUTUBE_API_KEY:
        print("\n❌ Error: You Must Insert Your Api Key")
        print("Follow The Instructions In Readme To Get An Api Key...")
        return
    
    scraper = YouTubeCommentsScraper(YOUTUBE_API_KEY)
    
    print("How Do You Want To Identify The Channel...?")
    print ("\n")
    print("1. Channel Name")
    print("2. Channel Url")
    print("3. Channel Id")
    
    choice = input("\nChoice: ").strip()
    
    channel_id = None
    
    if choice == '1':
        channel_input = input("\nEnter Channel Name: ").strip()
        channel_id = scraper.get_channel_id(channel_handle=channel_input)
    
    elif choice == '2':
        channel_url = input("\nEnter Channel Url: ").strip()
        channel_id = scraper.get_channel_id(channel_url=channel_url)
    
    elif choice == '3':
        channel_id = input("\nEnter Channel Id: ").strip()
    
    else:
        print("Invalid Choice!")
        return
    
    if not channel_id:
        print("\n❌ Unable To Find Channel. Verify The Entered Data.")
        return
    
    print(f"\n✓ Channel Id Found: {channel_id}")
    
    confirm = input("\nProceed With Comments Download...? ").strip().lower()
    
    if confirm not in ['y', 'yes']:
        print("Operation Cancelled.")
        return
    
    print("Download Started")
    
    all_comments, channel_name = scraper.scrape_channel_comments(channel_id)
    
    if not all_comments:
        print("\n⚠️ No Comments Found")
        return
    
    scraper.save_reports(all_comments, channel_name)
    
    print ("\n")

if __name__ == '__main__':
    main()
