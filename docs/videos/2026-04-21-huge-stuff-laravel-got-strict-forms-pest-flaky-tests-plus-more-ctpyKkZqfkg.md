# huge stuff: laravel got strict forms, pest flaky tests + more

URL: https://www.youtube.com/watch?v=ctpyKkZqfkg
Channel: [nunomaduro](https://www.youtube.com/@nunomaduro)
Upload date: 2026-04-21
Duration: 5:01
Status: auto-processed
Topics: laravel, testing

## Why This Helps Programming
This video appears to cover laravel, testing practices that can be reused in day-to-day programming work.

## Tips And Tricks
- And as you can see, most of the times it passes, but sometimes it actually fails because the GitHub API is a little bit flaky.
- Laravel 13.4 was also released this week and I'm very excited about this release because literally allows you to set up form requests as strict.
- Even though these fields were never requested, we just ignored them silently on the backend.
- By doing this, Laravel automatically will not anymore accept any fields that do not belong to the rules or field form request.
- In this example, if I try to send stuff that is not on the form request just like the name, this will actually cause my test to fail.
- And just for your big information, you may also use this attribute fail on unknown fields if used to either disable this feature for one form request or simply enable it for one form request only.
- But I don't have any queue, so this job will be dispatched but won't actually be consumed.

## Source Notes
- Tips are paraphrased or normalized from available YouTube captions/metadata.
- Video media is not stored in this repository.
