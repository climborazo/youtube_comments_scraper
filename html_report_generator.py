#!/usr/bin/env python3

import json
import sys
from datetime import datetime
from pathlib import Path

def generate_html_report(json_file: str, output_file: str = None):

    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            comments = json.load(f)
    except FileNotFoundError:
        print(f"❌ File Not Found: {json_file}")
        return
    except json.JSONDecodeError:
        print(f"❌ Error Parsing Json: {json_file}")
        return
    
    if not comments:
        print("❌ No Comments Found In Json File")
        return
    
    if not output_file:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'youtube_comments_report_{timestamp}.html'
    
    total_comments = len(comments)
    unique_authors = sorted(set(c['author'] for c in comments))
    unique_videos = len(set(c['video_id'] for c in comments))
    total_likes = sum(c['like_count'] for c in comments)
    replies_count = sum(1 for c in comments if c['is_reply'])
    top_level_count = total_comments - replies_count
    
    comments_json = json.dumps(comments, ensure_ascii=False)
    authors_json = json.dumps(unique_authors, ensure_ascii=False)
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Comments Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #0a0a0a;
            min-height: 100vh;
            padding: 20px;
            color: #e0e0e0;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: #1a1a1a;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            overflow: hidden;
            border: 1px solid #2a2a2a;
        }}
        
        .header {{
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            color: #ffffff;
            padding: 30px;
            text-align: center;
            border-bottom: 2px solid #3a3a3a;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-transform: capitalize;
            font-weight: 700;
            letter-spacing: 1px;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.8;
            text-transform: capitalize;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #141414;
            border-bottom: 2px solid #2a2a2a;
        }}
        
        .stat-card {{
            background: #1f1f1f;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 1px solid #2a2a2a;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(100,100,100,0.2);
            border-color: #3a3a3a;
        }}
        
        .stat-card .number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 5px;
        }}
        
        .stat-card .label {{
            color: #888888;
            font-size: 0.9em;
            text-transform: capitalize;
            letter-spacing: 1px;
        }}
        
        .filters {{
            padding: 30px;
            background: #1a1a1a;
            border-bottom: 2px solid #2a2a2a;
        }}
        
        .filters h2 {{
            margin-bottom: 20px;
            color: #ffffff;
            font-size: 1.5em;
            text-transform: capitalize;
        }}
        
        .filter-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .filter-group {{
            display: flex;
            flex-direction: column;
        }}
        
        .filter-group label {{
            font-weight: 600;
            margin-bottom: 8px;
            color: #b0b0b0;
            font-size: 0.9em;
            text-transform: capitalize;
        }}
        
        .filter-group input,
        .filter-group select {{
            padding: 12px;
            border: 1px solid #3a3a3a;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s ease;
            background: #0f0f0f;
            color: #e0e0e0;
        }}
        
        .filter-group input:focus,
        .filter-group select:focus {{
            outline: none;
            border-color: #555555;
            background: #1a1a1a;
        }}
        
        .filter-group input::placeholder {{
            color: #555555;
        }}
        
        .filter-actions {{
            display: flex;
            gap: 10px;
            margin-top: 15px;
            flex-wrap: wrap;
        }}
        
        .btn {{
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: capitalize;
        }}
        
        .btn-primary {{
            background: #2a2a2a;
            color: #ffffff;
            border: 1px solid #3a3a3a;
        }}
        
        .btn-primary:hover {{
            background: #3a3a3a;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(100,100,100,0.2);
        }}
        
        .btn-secondary {{
            background: #1a1a1a;
            color: #ffffff;
            border: 1px solid #3a3a3a;
        }}
        
        .btn-secondary:hover {{
            background: #2a2a2a;
        }}
        
        .btn-export {{
            background: #1a3a1a;
            color: #ffffff;
            border: 1px solid #2a4a2a;
        }}
        
        .btn-export:hover {{
            background: #2a4a2a;
        }}
        
        .results {{
            padding: 30px;
            background: #1a1a1a;
        }}
        
        .results-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #2a2a2a;
            flex-wrap: wrap;
            gap: 15px;
        }}
        
        .results-count {{
            font-size: 1.2em;
            color: #b0b0b0;
            text-transform: capitalize;
        }}
        
        .results-count strong {{
            color: #ffffff;
            font-size: 1.3em;
        }}
        
        .sort-options {{
            display: flex;
            gap: 10px;
            align-items: center;
        }}
        
        .sort-options label {{
            font-weight: 600;
            color: #b0b0b0;
            text-transform: capitalize;
        }}
        
        .sort-options select {{
            padding: 8px 12px;
            border: 1px solid #3a3a3a;
            border-radius: 6px;
            font-size: 0.9em;
            background: #0f0f0f;
            color: #e0e0e0;
        }}
        
        .comment-card {{
            background: #1f1f1f;
            border: 1px solid #2a2a2a;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            transition: all 0.3s ease;
        }}
        
        .comment-card:hover {{
            border-color: #3a3a3a;
            box-shadow: 0 5px 20px rgba(100,100,100,0.1);
        }}
        
        .comment-card.reply {{
            margin-left: 40px;
            border-left: 4px solid #3a3a3a;
            background: #1a1a1a;
        }}
        
        .comment-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 12px;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .comment-author {{
            font-weight: bold;
            color: #ffffff;
            font-size: 1.1em;
        }}
        
        .comment-meta {{
            display: flex;
            gap: 15px;
            align-items: center;
            color: #888888;
            font-size: 0.9em;
        }}
        
        .comment-date {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        
        .comment-likes {{
            display: flex;
            align-items: center;
            gap: 5px;
            color: #e74c3c;
        }}
        
        .comment-text {{
            color: #b0b0b0;
            line-height: 1.6;
            margin-bottom: 12px;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
        
        .comment-video {{
            background: #141414;
            padding: 10px 15px;
            border-radius: 8px;
            font-size: 0.9em;
            color: #888888;
            text-transform: capitalize;
        }}
        
        .comment-video strong {{
            color: #b0b0b0;
        }}
        
        .badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 600;
            text-transform: capitalize;
        }}
        
        .badge-reply {{
            background: #2a2a2a;
            color: #ffffff;
        }}
        
        .badge-top {{
            background: #1a3a1a;
            color: #ffffff;
        }}
        
        .no-results {{
            text-align: center;
            padding: 60px 20px;
            color: #888888;
        }}
        
        .no-results h3 {{
            font-size: 2em;
            margin-bottom: 10px;
            text-transform: capitalize;
        }}
        
        .loading {{
            text-align: center;
            padding: 40px;
            font-size: 1.2em;
            color: #ffffff;
            text-transform: capitalize;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8em;
            }}
            
            .filter-grid {{
                grid-template-columns: 1fr;
            }}
            
            .comment-card.reply {{
                margin-left: 20px;
            }}
            
            .results-header {{
                flex-direction: column;
                align-items: flex-start;
            }}
        }}
        
        .icon {{
            font-size: 1.2em;
        }}
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {{
            width: 10px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: #0a0a0a;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: #2a2a2a;
            border-radius: 5px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: #3a3a3a;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Youtube Comments Report</h1>
            <p>Interactive Comments Analysis</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="number">{total_comments}</div>
                <div class="label">Total Comments</div>
            </div>
            <div class="stat-card">
                <div class="number">{len(unique_authors)}</div>
                <div class="label">Unique Authors</div>
            </div>
            <div class="stat-card">
                <div class="number">{unique_videos}</div>
                <div class="label">Videos</div>
            </div>
            <div class="stat-card">
                <div class="number">{total_likes}</div>
                <div class="label">Total Likes</div>
            </div>
            <div class="stat-card">
                <div class="number">{top_level_count}</div>
                <div class="label">Main Comments</div>
            </div>
            <div class="stat-card">
                <div class="number">{replies_count}</div>
                <div class="label">Replies</div>
            </div>
        </div>
        
        <div class="filters">
            <h2>🔍 Search Filters</h2>
            <div class="filter-grid">
                <div class="filter-group">
                    <label for="searchText">Search Text</label>
                    <input type="text" id="searchText" placeholder="Keywords...">
                </div>
                <div class="filter-group">
                    <label for="searchAuthor">Search Author</label>
                    <select id="searchAuthor">
                        <option value="">All Authors</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label for="searchVideo">Search Video</label>
                    <input type="text" id="searchVideo" placeholder="Video Title...">
                </div>
                <div class="filter-group">
                    <label for="dateFrom">Date From</label>
                    <input type="date" id="dateFrom">
                </div>
                <div class="filter-group">
                    <label for="dateTo">Date To</label>
                    <input type="date" id="dateTo">
                </div>
                <div class="filter-group">
                    <label for="minLikes">Minimum Likes</label>
                    <input type="number" id="minLikes" placeholder="0" min="0">
                </div>
                <div class="filter-group">
                    <label for="commentType">Comment Type</label>
                    <select id="commentType">
                        <option value="all">All</option>
                        <option value="top">Main Comments Only</option>
                        <option value="replies">Replies Only</option>
                    </select>
                </div>
            </div>
            <div class="filter-actions">
                <button class="btn btn-primary" onclick="applyFilters()">🔎 Apply Filters</button>
                <button class="btn btn-secondary" onclick="resetFilters()">🔄 Reset</button>
                <button class="btn btn-export" onclick="exportResults()">💾 Export CSV</button>
            </div>
        </div>
        
        <div class="results">
            <div class="results-header">
                <div class="results-count">
                    Showing <strong id="resultsCount">0</strong> Comments
                </div>
                <div class="sort-options">
                    <label for="sortBy">Sort By:</label>
                    <select id="sortBy" onchange="applyFilters()">
                        <option value="date_desc">Date (Newest)</option>
                        <option value="date_asc">Date (Oldest)</option>
                        <option value="likes_desc">Likes (Most Popular)</option>
                        <option value="likes_asc">Likes (Least Popular)</option>
                        <option value="author_asc">Author (A-Z)</option>
                        <option value="author_desc">Author (Z-A)</option>
                    </select>
                </div>
            </div>
            <div id="commentsContainer">
                <div class="loading">Loading Comments...</div>
            </div>
        </div>
    </div>

    <script>
        // Comments data
        const allComments = {comments_json};
        const allAuthors = {authors_json};
        let filteredComments = [...allComments];
        
        // Populate authors dropdown
        function populateAuthorsDropdown() {{
            const select = document.getElementById('searchAuthor');
            allAuthors.forEach(author => {{
                const option = document.createElement('option');
                option.value = author;
                option.textContent = author;
                select.appendChild(option);
            }});
        }}
        
        // Format date
        function formatDate(dateString) {{
            const date = new Date(dateString);
            return date.toLocaleDateString('en-US', {{
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            }});
        }}
        
        // Apply filters
        function applyFilters() {{
            const searchText = document.getElementById('searchText').value.toLowerCase();
            const searchAuthor = document.getElementById('searchAuthor').value;
            const searchVideo = document.getElementById('searchVideo').value.toLowerCase();
            const dateFrom = document.getElementById('dateFrom').value;
            const dateTo = document.getElementById('dateTo').value;
            const minLikes = parseInt(document.getElementById('minLikes').value) || 0;
            const commentType = document.getElementById('commentType').value;
            const sortBy = document.getElementById('sortBy').value;
            
            // Filter
            filteredComments = allComments.filter(comment => {{
                // Text filter
                if (searchText && !comment.text.toLowerCase().includes(searchText)) {{
                    return false;
                }}
                
                // Author filter
                if (searchAuthor && comment.author !== searchAuthor) {{
                    return false;
                }}
                
                // Video filter
                if (searchVideo && !comment.video_title.toLowerCase().includes(searchVideo)) {{
                    return false;
                }}
                
                // Date from filter
                if (dateFrom) {{
                    const commentDate = new Date(comment.published_at).toISOString().split('T')[0];
                    if (commentDate < dateFrom) {{
                        return false;
                    }}
                }}
                
                // Date to filter
                if (dateTo) {{
                    const commentDate = new Date(comment.published_at).toISOString().split('T')[0];
                    if (commentDate > dateTo) {{
                        return false;
                    }}
                }}
                
                // Likes filter
                if (comment.like_count < minLikes) {{
                    return false;
                }}
                
                // Type filter
                if (commentType === 'top' && comment.is_reply) {{
                    return false;
                }}
                if (commentType === 'replies' && !comment.is_reply) {{
                    return false;
                }}
                
                return true;
            }});
            
            // Sort
            filteredComments.sort((a, b) => {{
                switch(sortBy) {{
                    case 'date_desc':
                        return new Date(b.published_at) - new Date(a.published_at);
                    case 'date_asc':
                        return new Date(a.published_at) - new Date(b.published_at);
                    case 'likes_desc':
                        return b.like_count - a.like_count;
                    case 'likes_asc':
                        return a.like_count - b.like_count;
                    case 'author_asc':
                        return a.author.localeCompare(b.author);
                    case 'author_desc':
                        return b.author.localeCompare(a.author);
                    default:
                        return 0;
                }}
            }});
            
            renderComments();
        }}
        
        // Reset filters
        function resetFilters() {{
            document.getElementById('searchText').value = '';
            document.getElementById('searchAuthor').value = '';
            document.getElementById('searchVideo').value = '';
            document.getElementById('dateFrom').value = '';
            document.getElementById('dateTo').value = '';
            document.getElementById('minLikes').value = '';
            document.getElementById('commentType').value = 'all';
            document.getElementById('sortBy').value = 'date_desc';
            applyFilters();
        }}
        
        // Render comments
        function renderComments() {{
            const container = document.getElementById('commentsContainer');
            const resultsCount = document.getElementById('resultsCount');
            
            resultsCount.textContent = filteredComments.length;
            
            if (filteredComments.length === 0) {{
                container.innerHTML = `
                    <div class="no-results">
                        <h3>😕 No Results</h3>
                        <p>Try Modifying The Search Filters</p>
                    </div>
                `;
                return;
            }}
            
            const html = filteredComments.map(comment => `
                <div class="comment-card ${{comment.is_reply ? 'reply' : ''}}">
                    <div class="comment-header">
                        <div>
                            <div class="comment-author">
                                ${{comment.author}}
                                ${{comment.is_reply ? '<span class="badge badge-reply">Reply</span>' : '<span class="badge badge-top">Comment</span>'}}
                            </div>
                        </div>
                        <div class="comment-meta">
                            <span class="comment-date">
                                <span class="icon">📅</span>
                                ${{formatDate(comment.published_at)}}
                            </span>
                            <span class="comment-likes">
                                <span class="icon">❤️</span>
                                ${{comment.like_count}}
                            </span>
                        </div>
                    </div>
                    <div class="comment-text">${{comment.text}}</div>
                    <div class="comment-video">
                        <strong>Video:</strong> ${{comment.video_title}}
                    </div>
                </div>
            `).join('');
            
            container.innerHTML = html;
        }}
        
        // Export to CSV
        function exportResults() {{
            const csvContent = [
                ['Author', 'Text', 'Likes', 'Date', 'Video', 'Type'],
                ...filteredComments.map(c => [
                    c.author,
                    c.text.replace(/"/g, '""'),
                    c.like_count,
                    c.published_at,
                    c.video_title.replace(/"/g, '""'),
                    c.is_reply ? 'Reply' : 'Comment'
                ])
            ].map(row => row.map(cell => `"${{cell}}"`).join(',')).join('\\n');
            
            const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'youtube_comments_filtered_' + new Date().toISOString().split('T')[0] + '.csv';
            link.click();
        }}
        
        // Load initially
        window.onload = function() {{
            populateAuthorsDropdown();
            applyFilters();
        }};
        
        // Auto-apply filters when typing
        document.getElementById('searchText').addEventListener('input', debounce(applyFilters, 500));
        document.getElementById('searchVideo').addEventListener('input', debounce(applyFilters, 500));
        document.getElementById('searchAuthor').addEventListener('change', applyFilters);
        
        // Debounce function
        function debounce(func, wait) {{
            let timeout;
            return function executedFunction(...args) {{
                const later = () => {{
                    clearTimeout(timeout);
                    func(...args);
                }};
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            }};
        }}
    </script>
</body>
</html>
"""
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Html Saved: {output_file}")
        print(f"\n📊 Comments Included: {total_comments}")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Error Saving Html File: {e}")
        return None


def main():
    """
    Cli Interface To Generate Html Report
    """
    print("="*60)
    print("Youtube Comments Html Report Generator")
    print("="*60)
    
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    else:
        json_file = input("\nEnter Path To Json File With Comments: ").strip()
    
    if not json_file:
        print("❌ You Must Specify A Json File")
        return
    
    if not Path(json_file).exists():
        print(f"❌ File Not Found: {json_file}")
        return
    
    custom_output = input("\nHTML Output Filename (Press Enter For Default): ").strip()
    
    if custom_output:
        output_file = custom_output if custom_output.endswith('.html') else f"{custom_output}.html"
    else:
        output_file = None
    
    generate_html_report(json_file, output_file)


if __name__ == '__main__':
    main()
