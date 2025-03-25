from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

GRID_SIZE = 5
start = None
end = None
obstacles = set()

directions = ['↑', '↓', '←', '→']
actions = {'↑': (-1, 0), '↓': (1, 0), '←': (0, -1), '→': (0, 1)}

@app.route("/")
def index():
    return render_template("index.html", grid_size=GRID_SIZE)

@app.route("/update_grid", methods=["POST"])
def update_grid():
    global start, end, obstacles, GRID_SIZE

    data = request.json
    row, col, cell_type = data["row"], data["col"], data["type"]
    GRID_SIZE = int(data.get("size", GRID_SIZE))

    if cell_type == "start":
        start = (row, col)
    elif cell_type == "end":
        end = (row, col)
    elif cell_type == "obstacle":
        if (row, col) in obstacles:
            obstacles.remove((row, col))
        elif len(obstacles) < GRID_SIZE - 2:
            obstacles.add((row, col))

    return jsonify({"start": start, "end": end, "obstacles": list(obstacles)})

@app.route("/generate_policy_and_value", methods=["POST"])
def generate_policy_and_value():
    global GRID_SIZE

    data = request.get_json()
    GRID_SIZE = int(data.get("size", GRID_SIZE))

    gamma = 0.9
    reward = -1
    max_iterations = 50

    policy = []
    for i in range(GRID_SIZE):
        row_policy = []
        for j in range(GRID_SIZE):
            if (i, j) in obstacles or (i, j) == end:
                row_policy.append('')
            else:
                legal_dirs = []
                for d, (di, dj) in actions.items():
                    ni, nj = i + di, j + dj
                    if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE and (ni, nj) not in obstacles:
                        legal_dirs.append(d)
                row_policy.append(random.choice(legal_dirs) if legal_dirs else '')
        policy.append(row_policy)

    value = [[0.0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    if end:
        value[end[0]][end[1]] = 0.0

    for _ in range(max_iterations):
        new_value = [[0.0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if (i, j) in obstacles or (i, j) == end or policy[i][j] == '':
                    continue
                di, dj = actions[policy[i][j]]
                ni, nj = i + di, j + dj
                if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE and (ni, nj) not in obstacles:
                    new_value[i][j] = reward + gamma * value[ni][nj]
                else:
                    new_value[i][j] = reward + gamma * value[i][j]
        value = new_value

    return jsonify({
        "policy": policy,
        "value": value,
        "start": start,
        "end": end,
        "obstacles": list(obstacles),
        "path": [],
        "size": GRID_SIZE
    })

@app.route("/value_iteration", methods=["POST"])
def value_iteration():
    global GRID_SIZE

    data = request.get_json()
    GRID_SIZE = int(data.get("size", GRID_SIZE))

    gamma = 0.9
    reward = -1
    max_iterations = 100
    theta = 1e-3

    value = [[0.0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    policy = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    if end:
        value[end[0]][end[1]] = 0.0

    for _ in range(max_iterations):
        delta = 0
        new_value = [[v for v in row] for row in value]
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if (i, j) in obstacles or (i, j) == end:
                    continue
                best_v = float('-inf')
                best_a = ''
                for a, (di, dj) in actions.items():
                    ni, nj = i + di, j + dj
                    if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE and (ni, nj) not in obstacles:
                        vs = reward + gamma * value[ni][nj]
                    else:
                        vs = reward + gamma * value[i][j]
                    if vs > best_v:
                        best_v = vs
                        best_a = a
                new_value[i][j] = best_v
                policy[i][j] = best_a
                delta = max(delta, abs(value[i][j] - best_v))
        value = new_value
        if delta < theta:
            break

       # 路徑追蹤（避免走進障礙或非法格子）
    path = []
    if start and end:
        visited = set()
        cur = start
        while cur != end and cur not in visited:
            visited.add(cur)

            # 若此格無行動（policy 空或障礙），結束追蹤
            if cur in obstacles or policy[cur[0]][cur[1]] == '':
                break

            path.append(cur)
            action = policy[cur[0]][cur[1]]
            if action not in actions:
                break

            di, dj = actions[action]
            ni, nj = cur[0] + di, cur[1] + dj

            # 若下一步非法（超出範圍或進入障礙物），中止追蹤
            if not (0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE):
                break
            if (ni, nj) in obstacles:
                break

            cur = (ni, nj)

        # 若成功抵達終點，才把終點加進去
        if cur == end:
            path.append(end)


    return jsonify({
        "policy": policy,
        "value": value,
        "start": start,
        "end": end,
        "obstacles": list(obstacles),
        "path": path,
        "size": GRID_SIZE
    })

if __name__ == "__main__":
    app.run(debug=True)
