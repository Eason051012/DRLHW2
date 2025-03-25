let gridSize = 5;
let startSet = false;
let endSet = false;
let obstacleCount = 0;

function generateGrid() {
    gridSize = parseInt(document.getElementById("grid-size").value);
    startSet = false;
    endSet = false;
    obstacleCount = 0;

    const grid = document.getElementById("grid");
    grid.innerHTML = "";
    grid.style.gridTemplateColumns = `repeat(${gridSize}, 50px)`;
    grid.style.display = "grid";

    for (let i = 0; i < gridSize; i++) {
        for (let j = 0; j < gridSize; j++) {
            const cell = document.createElement("div");
            cell.classList.add("cell");
            cell.dataset.row = i;
            cell.dataset.col = j;
            cell.textContent = i * gridSize + j + 1;
            cell.onclick = () => handleClick(cell, i, j);
            grid.appendChild(cell);
        }
    }

    document.getElementById("policy-matrix").innerHTML = "";
    document.getElementById("value-matrix").innerHTML = "";
}

function handleClick(cell, row, col) {
    let type = "";

    if (!startSet) {
        cell.classList.add("start");
        startSet = true;
        type = "start";
    } else if (!endSet) {
        cell.classList.add("end");
        endSet = true;
        type = "end";
    } else {
        if (cell.classList.contains("obstacle")) {
            cell.classList.remove("obstacle");
            obstacleCount--;
        } else if (obstacleCount < gridSize - 2) {
            cell.classList.add("obstacle");
            obstacleCount++;
        } else {
            alert("最多只能選擇 " + (gridSize - 2) + " 個障礙物！");
            return;
        }
        type = "obstacle";
    }

    $.ajax({
        url: "/update_grid",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({ row, col, type, size: gridSize }),
    });
}

function renderMatrices(res) {
    const size = res.size;
    const policyDiv = document.getElementById("policy-matrix");
    const valueDiv = document.getElementById("value-matrix");

    policyDiv.style.gridTemplateColumns = `repeat(${size}, 50px)`;
    valueDiv.style.gridTemplateColumns = `repeat(${size}, 50px)`;
    policyDiv.innerHTML = "";
    valueDiv.innerHTML = "";

    for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
            const p = document.createElement("div");
            const v = document.createElement("div");
            p.className = "cell";
            v.className = "cell";

            if (res.start && res.start[0] === i && res.start[1] === j) {
                p.classList.add("start");
                v.classList.add("start");
            } else if (res.end && res.end[0] === i && res.end[1] === j) {
                p.classList.add("end");
                v.classList.add("end");
            } else if (res.obstacles.some(o => o[0] === i && o[1] === j)) {
                p.classList.add("obstacle");
                v.classList.add("obstacle");
            }

            if (res.path && res.path.some(pth => pth[0] === i && pth[1] === j)) {
                p.classList.add("path");
                v.classList.add("path");
            }

            p.textContent = res.policy[i][j] || '';
            if (!res.obstacles.some(o => o[0] === i && o[1] === j)) {
                v.textContent = res.value[i][j].toFixed(2);
            }

            policyDiv.appendChild(p);
            valueDiv.appendChild(v);
        }
    }
}

function generatePolicyAndValue() {
    $.ajax({
        url: "/generate_policy_and_value",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({ size: gridSize }),
        success: renderMatrices
    });
}

function runValueIteration() {
    $.ajax({
        url: "/value_iteration",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({ size: gridSize }),
        success: renderMatrices
    });
}

window.onload = generateGrid;
