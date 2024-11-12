from django.http import StreamingHttpResponse
import time
import json
from . import solver

def sse_view(request):
    def event_stream(puzzle_positions):
        print('puzzle_positions')
        puzzle_positions_json = json.loads(puzzle_positions)
        for solution in solver.solvePuzzle(puzzle_positions_json):
            result = solver.turn_board_to_front(solution)
            yield f"data: {json.dumps(result)}\n\n"
            time.sleep(1)

    puzzle_positions = request.GET.get('positions', '[]')
    response = StreamingHttpResponse(event_stream(puzzle_positions), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response

