from flask import Flask, render_template, request, jsonify
import json
import os
from difflib import SequenceMatcher

app = Flask(__name__)

# 讀取 classes.json
with open("./classes.json", "r", encoding="utf-8") as f:
    classes = json.load(f)

# JSON 檔案路徑
JSON_FILE_PATH = "./分類後.json"
# 加載 JSON 資料
def load_json_data():
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        return {}
    
def save_json_data(data):
    """保存 JSON 數據"""
    with open(JSON_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

@app.route("/")
def index():
    return render_template("index.html", classes=classes)

@app.route("/set")
def _set():
    return render_template("set.html", classes=classes)

@app.route("/select", methods=["POST"])
def select():
    data = request.json
    key = data.get("key")
    sub_key = data.get("sub_key", "nosub")  # 預設使用 "nosub"
    if key > "9":
        sub_key = key
        key = "0"
    
    # 加載 JSON 資料
    json_data = load_json_data()

    # 找到主類和子類對應的症狀
    symptoms = []
    if key and key in json_data:
        if sub_key in json_data[key]:
            symptoms = json_data[key][sub_key]
        elif "nosub" in json_data[key]:
            symptoms = json_data[key]["nosub"]

    # 回傳對應資料給前端
    return jsonify({
        "key": key,
        "sub_key": sub_key,
        "symptoms": symptoms
    })

# 預先讀取 JSON 檔案
with open("./證候_症狀.json", "r", encoding="utf-8") as file:
    zh_hou_symptoms = json.load(file)

def calculate_similarity(a, b):
    """計算兩個字串的相似度"""
    return SequenceMatcher(None, a, b).ratio()

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    Symptoms = data.get("selectedSymptoms")
    
    if not Symptoms:
        return jsonify({"error": "未選擇症狀"}), 400

    # 將症狀轉成字串，用逗號分隔
    Symptoms_str = ",".join(Symptoms)
    # 進行相似度比對
    results = []
    for key, value in zh_hou_symptoms.items():
        sym_list = value.split(", ")
        similarity = 0
        for q_symptoms in Symptoms:
            for v_Symptoms in sym_list:
                ratio = calculate_similarity(q_symptoms, v_Symptoms)
                similarity += ratio
        similarity /= (len(Symptoms)*len(sym_list))
        results.append((key, similarity))

    # 按相似度排序，取前三個
    top_3 = sorted(results, key=lambda x: x[1], reverse=True)[:3]
    print(top_3)
    # 回傳結果給前端
    return jsonify({"top_3": [{"text": item[0], "similarity": item[1]} for item in top_3]})


@app.route('/search', methods=['POST'])
def search_symptoms():
    query = request.json.get('query', '').strip()
    if not query:
        return jsonify({"symptoms": []})

    # 從 JSON 數據中查詢
    json_data = load_json_data()
    results = set()

    for key, value in json_data.items():
        for category, items in value.items():
            if isinstance(items, list):  # 確保數據是列表
                for item in items:
                    if query in item:  # 如果關鍵字出現在數據中
                        results.add(item)

    return jsonify({"symptoms": list(results)})

@app.route('/modify_category', methods=['POST'])
def modify_category():
    data = request.json
    if data:
        symptom = data["symptom"]
        new_main_category = data["new_main_category"]
        new_sub_category = data["new_sub_category"]
        json_data = load_json_data()
        # 遍歷 json_data，刪除與 data 相同的字串
        for key, val in json_data.items():
            for category, symptoms in val.items():
                if symptom in symptoms:
                    symptoms.remove(symptom)
        
        if new_main_category == "":
            new_main_category = "0"
        if new_sub_category == "":
            new_sub_category = "nosub"
        json_data[new_main_category][new_sub_category].append(symptom)
        # 保存修改後的數據
        save_json_data(json_data)
        return jsonify({"ok": True, "message": f"症狀 '{data}' 已修改"})
    #舌苔燥黑
    return jsonify({"ok": False, "message": "請提供有效的症狀"}), 400

@app.route('/delete_symptom', methods=['POST'])
def delete_symptom():
    data = request.json.get("symptom", "")
    if data:
        json_data = load_json_data()
        # 遍歷 json_data，刪除與 data 相同的字串
        for key, val in json_data.items():
            for category, symptoms in val.items():
                if data in symptoms:
                    symptoms.remove(data)

        # 保存修改後的數據
        save_json_data(json_data)
        return jsonify({"ok": True, "message": f"症狀 '{data}' 已刪除"})
    #舌苔燥黑
    return jsonify({"ok": False, "message": "請提供有效的症狀"}), 400

if __name__ == "__main__":
    app.run(debug=True)


