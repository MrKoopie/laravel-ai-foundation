# The Action Pattern Is Key to Clean Code

URL: https://www.youtube.com/watch?v=k_gMfdpSXQE
Channel: [nunomaduro](https://www.youtube.com/@nunomaduro)
Upload date: 2026-06-03
Duration: 9:40
Status: manual-processed
Topics: architecture, clean-code

## Why This Helps Programming
Explains the Laravel action pattern as a way to keep controllers thin, isolate application behavior, and make business workflows reusable outside HTTP requests.

## Tips And Tricks
- Move application behavior into action classes instead of packing it into controllers.
- Keep HTTP concerns out of actions; pass plain validated data rather than request objects.
- Use form requests at the boundary, then call `validated()` before handing data to an action.
- Wrap multi-step mutations in a transaction so partial updates roll back together.
- Reuse actions from controllers, jobs, commands, or other actions when the same behavior is needed in multiple entry points.
- Use arrays or DTOs deliberately for action input; choose the structure that makes the boundary clear without overcomplicating the call site.

## Source Notes
- Tips are paraphrased or normalized from available YouTube captions/metadata.
- Video media is not stored in this repository.
