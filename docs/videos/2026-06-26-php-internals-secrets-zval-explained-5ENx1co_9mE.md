# PHP Internals Secrets: ZVAL Explained

URL: https://www.youtube.com/watch?v=5ENx1co_9mE
Channel: [nunomaduro](https://www.youtube.com/@nunomaduro)
Upload date: 2026-06-26
Duration: 9:18
Status: auto-processed
Topics: php

## Why This Helps Programming
This video appears to cover php practices that can be reused in day-to-day programming work.

## Tips And Tricks
- Make sure you watch the entire video because the announcement is totally worth it.
- If you combine these names, actually comes Zend, which I don't know if originally the idea was that, but I just found that interesting.
- And then we have this unsigned integer of eight bytes, and something important to keep in mind is that when you work with PHP, you don't actually specify an integer is unsigned or how many bytes it can hold.
- However, when you code on C, you kind of have to be specific with the memory you allocate for anything cuz you really need to be super memory optimized.
- It doesn't always happens like that.
- I explained how to compile PHP and more, but let's actually use make to compile PHP and on the flag {dash} G, let's actually specify how many cores we have to make the process a little bit faster.
- Then we use the debug Zval dump, which is the function we just modified to print a little bit more about the Zend value.
- We see type tag equals to four, meaning that this Zval should be a long, as you can see here.

## Source Notes
- Tips are paraphrased or normalized from available YouTube captions/metadata.
- Video media is not stored in this repository.
