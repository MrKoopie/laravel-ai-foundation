# Laravel Clean Code: Invokable Controllers, Form Requests, Jobs, and More

URL: https://www.youtube.com/watch?v=ZdzdOcdRowk
Channel: [nunomaduro](https://www.youtube.com/@nunomaduro)
Upload date: 2025-12-26
Duration: 12:35
Status: auto-processed
Topics: clean-code, laravel

## Why This Helps Programming
This video appears to cover clean-code, laravel practices that can be reused in day-to-day programming work.

## Tips And Tricks
- It doesn't make sense to be create because it's a post request but the store doesn't make sense either because I'm not storing the exportation.
- For me th those are the cases where it's kind of it's kind of telling me the code is screaming at me that this should be an invocable action.
- For me like actions should be um independent from the HTTP layer.
- >> It means that it should be done before the action in on the controller itself because the controller is responsible for the HTTP layer and within the action I mean we can jump into that real quick.
- There is something I always do that nobody does, which is setting the minimum expectations for literals.
- >> The name might not be a good example because someone may be named X apparently or Z.
- Let's go with 50 or 80, you know, like let's give a minimum sensitive default >> to make sure >> names have some sort of thing that fits the UI to everyone without actually having to bug the designer to be careful about everything.
- That's what I do typically and I do the same thing with everything else like with age for example um you know I ensure it's bigger than one in less depending of the use case of course but less than 200 for example.

## Source Notes
- Tips are paraphrased or normalized from available YouTube captions/metadata.
- Video media is not stored in this repository.
