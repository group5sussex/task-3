from django.http import StreamingHttpResponse
import time
import json

def sse_view(request):
    def event_stream(puzzle_positions):
        for i in range(5):  # Assume 5 solutions for demonstration
            time.sleep(1)
            solution = f"Solution {i+1} for positions {puzzle_positions}"
            yield f"data: {json.dumps(solution)}\n\n"

    puzzle_positions = request.GET.get('positions', '[]')
    response = StreamingHttpResponse(event_stream(puzzle_positions), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response

