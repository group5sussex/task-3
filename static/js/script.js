let selectedPiece = null;

let dragData = null;

let shapes = [
    [[1, 1, 1], [1, 0, 1]],
    [[0, 0, 2, 2], [2, 2, 2, 0]],
    [[0, 3, 0], [3, 3, 0], [0, 3, 3]],
    [[0, 4, 0], [4, 4, 4]],
    [[0, 5, 0, 0], [5, 5, 5, 5]],
    [[0, 6, 6], [6, 6, 6]],
    [[0, 7, 7], [7, 7, 0]],
    [[8, 8], [8, 0], [8, 0]],
    [[9, 9, 9], [0, 0, 9], [0, 0, 9]],
    [[10, 0, 0, 0], [10, 10, 10, 10]],
    [[0, 11], [11, 11]],
    [[12, 12, 0], [0, 12, 12], [0, 0, 12]]
];

let vBoard = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
];

let infoPiecesInBoard = [
    [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]
];

let pieceUsed = [false, false, false, false, false, false, false, false, false, false, false, false];

let tempBoard = JSON.parse(JSON.stringify(vBoard));

let dragCounter = 0;

document.querySelectorAll('.piece').forEach(piece => {
    piece.addEventListener('dragstart', dragStart);
    piece.addEventListener('drag', drag);
    piece.addEventListener('dragend', ()=> {
        dragData = null; dragCounter = 0; selectedPiece = null;
    })
});

function rotatePieceDuringDrag(e, selectedPiece) {
    const piece = selectedPiece;
    let rotation = parseInt(piece.getAttribute('data-rotation') || '0');
    rotation += 90;
    rotation = (rotation + 360) % 360; // Ensure rotation is always positive
    piece.setAttribute('data-rotation', rotation);
    dragData.rotation = rotation;
}


let lastRotationTime = 0;
const debounceTime = 200;
function drag(e) {
    if (!dragData && !selectedPiece) return;

    const currentTime = Date.now();
    if (e.shiftKey && currentTime - lastRotationTime > debounceTime) {
        rotatePieceDuringDrag(e, selectedPiece);
        lastRotationTime = currentTime;
    } else if (e.altKey && currentTime - lastRotationTime > debounceTime) {
        mirrorPieceDuringDrag(e, selectedPiece);
        lastRotationTime = currentTime;
    }

    dragData.rotation = selectedPiece.getAttribute('data-rotation');
    dragData.mirrored = selectedPiece.getAttribute('data-mirrored');

    transformPiece(selectedPiece, dragData.rotation, dragData.mirrored);

    const dragImage = createDragImage(selectedPiece, dragData.rotation, dragData.mirrored);
    document.body.appendChild(dragImage);
    e.dataTransfer.setDragImage(dragImage, 0, 0);

    setTimeout(() => {
        dragImage.remove();
    }, 0);
}

function mirrorPieceDuringDrag(e, selectedPiece) {
    const piece = selectedPiece;
    let mirrored = piece.getAttribute('data-mirrored') || '0';
    mirrored = mirrored === '1' ? '0' : '1';
    piece.setAttribute('data-mirrored', mirrored);
    dragData.mirrored = mirrored;
}

document.querySelectorAll('.cell').forEach(cell => {
    cell.setAttribute('draggable', 'true');
    cell.addEventListener('dragover', dragOver);
    cell.addEventListener('drop', dropPiece);

    cell.addEventListener('dragleave', changeCell); // Clear preview when leaving
    cell.addEventListener('dragenter', previewPiece); // New preview event

    cell.addEventListener('dragstart', startDragOutFromBoard);
    cell.addEventListener('drag', drag);
    cell.addEventListener('dragend', dragEnd);
});

function dragEnd(e) {
    pieceUsed[dragData.shapeId - 1] = false;
    document.getElementById(`piece${dragData.shapeId}`).style.backgroundColor = 'transparent';
}

document.getElementById('board').addEventListener('dragenter', (e) => {
    dragCounter++;
});

document.getElementById('board').addEventListener('dragleave', (e) => {
    dragCounter--;
    if (dragCounter === 0) {
        clearView(e);
    }
});

function previewPiece(e) {
    e.preventDefault();
    if (!dragData) return;
    const cell = e.target;
    const { shapeId, rotation, mirrored } = dragData;

    const shape = shapes[parseInt(shapeId) - 1];
    const x = parseInt(cell.id) % 11;
    const y = Math.floor(parseInt(cell.id) / 11);
    const filler = parseInt(shapeId);
    tempBoard = JSON.parse(JSON.stringify(vBoard));
    tempBoard = putPiece(shape, x, y, filler, tempBoard, parseInt(rotation), parseInt(mirrored));
    drawBoard(tempBoard);
}

function changeCell(e) {

    e.preventDefault();

    drawBoard(tempBoard); // Revert back to the original board state
}

function clearView(e) {
    e.preventDefault();
    drawBoard(vBoard);
}

function startDragOutFromBoard(e) {
    const cell = e.target;

    const shapeId = vBoard[Math.floor(cell.id / 11)][cell.id % 11];
    if (shapeId === 0) return e.preventDefault();
    vBoard = removePiece(vBoard, shapeId);
    drawBoard(vBoard);

    const piece = document.getElementById(`piece${shapeId}`);
    let rotation = infoPiecesInBoard[shapeId - 1][0];
    let mirrored = infoPiecesInBoard[shapeId - 1][1];

    setDragMetaInfo(e, rotation, mirrored, piece);

}

function removePiece(board, shapeId) {
    let boardCopy = JSON.parse(JSON.stringify(board));
    for (let i = 0; i < boardCopy.length; i++) {
        for (let j = 0; j < boardCopy[i].length; j++) {
            if (boardCopy[i][j] === shapeId) {
                boardCopy[i][j] = 0;
            }
        }
    }
    return boardCopy;
}

function rotatePiece(e) {
    console.log('rotatePiece');
    e.preventDefault();
    const piece = e.target;
    let rotation = parseInt(piece.getAttribute('data-rotation') || '0');
    const mirrored = piece.getAttribute('data-mirrored') || '0';

    rotation += e.deltaY > 0 ? 90 : -90;
    rotation = (rotation + 360) % 360; // Ensure rotation is always positive

    piece.setAttribute('data-rotation', rotation);

    transformPiece(piece, rotation, mirrored);
}

function mirrorPiece(e) {
    e.preventDefault();
    const piece = e.target;
    let rotation = parseInt(piece.getAttribute('data-rotation') || '0');
    let mirrored = piece.getAttribute('data-mirrored') || '0';

    mirrored = mirrored === '1' ? '0' : '1';
    piece.setAttribute('data-mirrored', mirrored);

    transformPiece(piece, rotation, mirrored);
}

function transformPiece(piece, rotation, mirrored) {
    const scaleX = mirrored === '1' ? -1 : 1;
    piece.childNodes[0].style.transform = `rotate(${rotation}deg)`;
    piece.style.transform = `scaleX(${scaleX})`;

}

function dragStart(e) {
    const piece = e.target;
    if (pieceUsed[parseInt(piece.dataset.shape) - 1]) return e.preventDefault();
    const rotation = piece.getAttribute('data-rotation') || '0';
    const mirrored = piece.getAttribute('data-mirrored') || '0';

    setDragMetaInfo(e, rotation, mirrored, piece);
    selectedPiece = piece;
}

function setDragMetaInfo(e, rotation, mirrored, piece) {
    e.dataTransfer.setData('text/plain', JSON.stringify({
        shapeId: piece.dataset.shape,
        rotation: rotation,
        mirrored: mirrored,
    }));

    dragData = {
        shapeId: piece.dataset.shape,
        rotation: rotation,
        mirrored: mirrored,
    };

    const dragImage = createDragImage(piece, rotation, mirrored);
    document.body.appendChild(dragImage);
    e.dataTransfer.setDragImage(dragImage, 0, 0);

    setTimeout(() => {
        dragImage.remove();
    }, 0);
}

function createDragImage(piece, rotation, mirrored) {
    const dragImage = piece.cloneNode(true);
    dragImage.style.position = 'absolute';
    const adjustedScaleX = (mirrored !== '1' ? 'scaleX(1)' : rotation === '90' || rotation === '270' ? 'scaleY(-1)' : 'scaleX(-1)');
    dragImage.childNodes[0].style.transform = `rotate(${rotation}deg) ${adjustedScaleX}`;

    dragImage.style.top = '-1000px';
    dragImage.style.left = '-1000px';
    return dragImage;
}

function dragOver(e) {
    e.preventDefault();
}

function dropPiece(e) {
    e.preventDefault()
    const cell = e.target;
    const data = dragData;
    const { shapeId, rotation, mirrored } = data;

    const shape = shapes[parseInt(shapeId)-1];
    const x = parseInt(cell.id) % 11;
    const y = Math.floor(parseInt(cell.id) / 11);
    const filler = parseInt(shapeId);

    vBoard = putPiece(shape, x, y, filler, vBoard, parseInt(rotation), parseInt(mirrored));

    drawBoard(vBoard);

    dragData = null; dragCounter = 0; infoPiecesInBoard[filler - 1] = [parseInt(rotation), parseInt(mirrored)];
    pieceUsed[filler - 1] = true; document.getElementById(`piece${filler}`).style.backgroundColor = 'black';
}

document.getElementById('reset').addEventListener('click', resetBoard);

function resetBoard() {
    vBoard = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ];
    infoPiecesInBoard = [
        [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]
    ];
    pieceUsed = [false, false, false, false, false, false, false, false, false, false, false, false];

    document.querySelectorAll('.piece').forEach(piece => {
        piece.style.backgroundColor = 'transparent';
    });

    solutions = [];

    document.getElementsByClassName("solution-changer")[0].style.transform = "scaleX(0)";

    current_solution = 0;

    first_load = false

    close_connection();

    drawBoard(vBoard);
}

function putPiece(shape, x, y, filler, vBoard, rotation = 0, mirrored = 0) {
    let vBoardCopy = JSON.parse(JSON.stringify(vBoard));

    if (rotation < 0) {
        rotation = 360 + rotation;
    }

    let shapeCopy = JSON.parse(JSON.stringify(shape));
    for (let i = 0; i < rotation / 90; i++) {
        shapeCopy = rotate90Clockwise(shapeCopy);
    }
    if (mirrored) {
        shapeCopy = mirrorByYAxis(shapeCopy);
    }

    for (let i = 0; i < shapeCopy.length; i++) {
        for (let j = 0; j < shapeCopy[i].length; j++) {
            if (!shapeCopy[i][j]) {
                continue;
            }
            if (vBoardCopy[y + i][x + j] !== 0) {
                return vBoard;
            }
            vBoardCopy[y + i][x + j] = filler;
        }
    }

    return vBoardCopy;
}

let colors = {
    1: 'rgba(0,95,115,255)',
    2: 'rgba(10,147,150,255)',
    3: 'rgba(148,210,189,255)',
    4: 'rgba(233,216,166,255)',
    5: 'rgba(238,155,0,255)',
    6: 'rgba(238,155,0,255)',
    7: 'rgba(187,62,3,255)',
    8: 'rgba(187,62,3,255)',
    9: 'rgba(155,34,38,255)',
    10: 'rgba(164,54,58,255)',
    11: 'rgba(199,101,44,255)',
    12: 'rgba(210,139,85,255)'
}

function drawBoard(vBoard) {
    let tempBoard = JSON.parse(JSON.stringify(vBoard));

    for (let i = 0; i < 12; i++) {
        document.getElementById(`piece${i+1}`).style.backgroundColor = 'transparent';
        pieceUsed[i] = false;
    }

    for (let i = 0; i < tempBoard.length; i++) {
        for (let j = 0; j < tempBoard[i].length; j++) {
            const cell = document.getElementById(`${j + i * 11}`);
            if (!tempBoard[i][j]) {
                cell.style.backgroundColor = `#fff`;
                cell.dataset.filler = '0';
                continue;
            }
            cell.style.backgroundColor = colors[tempBoard[i][j]];
            cell.dataset.filler = tempBoard[i][j];
            pieceUsed[tempBoard[i][j] - 1] = true;
            document.getElementById(`piece${tempBoard[i][j]}`).style.backgroundColor = 'black';
        }
    }
}

function rotate90Clockwise(matrix) {
    const rows = matrix.length;
    const cols = matrix[0].length;
    const rotated = Array.from({ length: cols }, () => Array(rows));

    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            rotated[j][rows - 1 - i] = matrix[i][j];
        }
    }
    return rotated;
}

function mirrorByYAxis(matrix) {
    return matrix.map(row => row.reverse());
}


