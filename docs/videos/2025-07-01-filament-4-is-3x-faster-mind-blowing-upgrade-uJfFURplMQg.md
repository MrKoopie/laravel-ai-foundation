# FILAMENT 4 is 3x FASTER?! Mind-Blowing Upgrade!

URL: https://www.youtube.com/watch?v=uJfFURplMQg
Channel: [nunomaduro](https://www.youtube.com/@nunomaduro)
Upload date: 2025-07-01
Duration: 15:41
Status: auto-processed
Topics: laravel

## Why This Helps Programming
This video appears to cover laravel practices that can be reused in day-to-day programming work.

## Tips And Tricks
- U I don't think Nuno knew this was one of the demos that I was going to give.
- That's actually you know every time I you know I I see a a new library getting a new version that's something always welcomed basically and I feel like for filament you were needing this and I really appreciate your work on this man.
- We don't change that because any modal can have any content of components inside uh any components inside of it.
- We do make a server request to render the content of the modal because it's just more efficient for us to do that.
- However, in filament 3, what happens when you click a modal is it's going to make a request to the server and because it's a LiveWire component, it's going to render the entire live component.
- It's 100 milliseconds and that is because um even though these are both the same live wire component we have created a partial rendering extension for livewire.
- How this works is instead of sending through the entire HTML for the liveware component, we are only sending through a part of the liveware component to the front end in this partials part of the response.
- Doing so means that as well as avoiding rendering the rest of the HTML and sending it through, we can avoid any database queries or anything that are required to render the rest of it.

## Source Notes
- Tips are paraphrased or normalized from available YouTube captions/metadata.
- Video media is not stored in this repository.
