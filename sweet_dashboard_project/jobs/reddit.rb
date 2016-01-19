require 'net/http'
require 'json'


class Reddit
   
    def getTopPostsPerSubreddit()  
        
        uri = URI("http://0.0.0.0:8080/api/")
        response = Net::HTTP.get(uri)
        #puts response
        data = JSON.parse(response)
        subreddit =Array.new
    
        for d in data
            subreddit = d['reddit']
        end
        response = []
        posts = [];
        #print subreddit
        for it in subreddit
            puts it
            url = URI("https://www.reddit.com"+it+"/.json")
            data = Net::HTTP.get(url)
            response = JSON.parse(data)
            
            items = []
            mastr_ar = response['data']['children']
            
            for item_ in mastr_ar[0..4]
                title = item_['data']['title']
                trimmed_title = title[0..85].gsub(/\s\w+$/, '...')
                items.push({
                    title: trimmed_title,
                    score: item_['data']['score'],
                    comments: item_['data']['num_comments']
                })
            end
            posts.push({ label: 'Current top posts in "' + it + '"', items: items })
        end
     posts
    end
end

@Reddit = Reddit.new();

SCHEDULER.every '20s', :first_in => 0 do |job|
  
  posts = @Reddit.getTopPostsPerSubreddit
   
  send_event('reddit', { :posts => posts })
end		
			