let solutions = [];
let current_solution = 0;

let eventSource = null;

let first_load = false;

document.getElementsByClassName("solution-changer")[0].style.transform = "scaleX(0)";

function transform_to_backend(vBoard) {
    let result = {};
    for (let i = 0; i < 5; i++) {
        for (let j = 0; j < 11; j++) {
            if (vBoard[i][j] === 0) continue;
            if (!result[vBoard[i][j] - 1]) {
                result[vBoard[i][j] - 1] = [];
            }
            result[vBoard[i][j] - 1].push([i,j]);
        }
    }
    return result;
}

function transform_to_frontend(data) {
    let result = [];
    for (let i = 0; i < 5; i++) {
        result.push([]);
        for (let j = 0; j < 11; j++) {
            result[i].push(0);
        }
    }
    for (let key in data) {
        for (let i = 0; i < data[key].length; i++) {
            result[data[key][i][0]][data[key][i][1]] = parseInt(key) + 1;
        }
    }
    return result;

}

function send_data(){
    let data = transform_to_backend(vBoard);

    console.log(data)

    close_connection()

    eventSource = startSSE(JSON.stringify(data), onMessage, onError);

    document.getElementsByClassName("solution-changer")[0].style.transform = "scaleX(0)";
}

function close_connection(){
    if (eventSource) {
        eventSource.close();
        eventSource = null;
    }

}

function startSSE(data, onMessage, onError) {
    const eventSource = new EventSource(`/events/?positions=${encodeURIComponent(data)}`);

    eventSource.onmessage = onMessage;

    eventSource.onerror = onError;

    return eventSource;
}

function onMessage(event) {
    const solution = JSON.parse(event.data);
    let result = transform_to_frontend(solution);
    if (solutions.some(solution => JSON.stringify(solution) === JSON.stringify(result))) return;
    solutions.push(result);
    if (!first_load) {
        load_solution(result);
        first_load = true;
    }
    document.getElementsByClassName("solution-changer")[0].style.transform = "scaleX(1)";
}

function onError(event) {
    console.error("EventSource failed:", event);
    close_connection();
}

function load_solution(board){
    vBoard = board;
    drawBoard(vBoard);
}

function change_solution(i){
    load_solution(solutions[i]);
    document.getElementById("solution").innerText = i + 1;
    current_solution = i;
}

document.getElementById("solve").addEventListener("click", send_data);

document.getElementById("next").addEventListener("click", () => {
    if (current_solution > solutions.length - 1) return;
    change_solution(current_solution + 1);
});

document.getElementById("prev").addEventListener("click", () => {
    if (current_solution < 1) return;
    change_solution(current_solution - 1);
    
});