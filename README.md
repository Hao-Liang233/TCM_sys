# TCM_sys

## 簡介
該程式主要透過Flask架設簡易網站，做到與User互動的效果來設定和查詢症狀症候，在前端與後端的資料傳輸方面，目前是直接透過Flask將資料丟到前端。  
建議可以改成透過get或post的方式將相關資料傳到前端。

## 主程式說明(main.py)  
```submit function```相似度函數，目前透過SequenceMatcher比對輸入症狀和```證候_症狀.json```中所有的症狀。  
除此之外的函數都是對資料做刪除修改等操作。

---
測試用網頁：  
https://tcm-sys.onrender.com  
(由於是免費服務，啟動需要等待較長時間)
## 檔案結構
```
│  app.py           主程式
│  classes.json     類別管理
│  Procfile
│  README.md
│  requirements.txt 套件版本
│  runtime.txt      程式版本
│  分類後.json       整理後的類別
│  證候_症狀.json    原始症狀
|  證候 症狀_繁體中文.xlsx 原始資料的繁體中文版
│
├─static            
│  ├─css
│  │      index.css
│  │
│  ├─img
│  │      python-file.png
│  │
│  └─js
│          jquery.min.js
│
└─templates
        index.html  主網頁面
        set.html    設定症狀頁面
```



---
### classes.json：
第一層為主類別，例如：1,2,3,4,...D,E。  
主類別中的Sub為子類別
```
{
    "1": {
      "name": "頭部",
      "Sub": {
        "F": "面部",
        "G": "眼睛",
        "H": "耳朵",
        "I": "口",
        "J": "腦子",
        "K": "唇",
        "L": "齒",
        "d": "鼻子"
      }
    },
    "2": {
      "name": "頸部",
      "Sub": {
        "M": "喉嚨",
        "N": "氣管",
        "O": "食道"
      }
    },
    "3": {
      "name": "胸部",
      "Sub": {
        "P": "心臟",
        "Q": "肺臟"
      }
    },
    "4": {
      "name": "四肢",
      "Sub": {
        "R": "手",
        "S": "腳"
      }
    },
    "5": {
      "name": "腹部",
      "Sub": {
        "T": "胃",
        "U": "小腸",
        "V": "大腸",
        "W": "腎臟",
        "X": "脾臟",
        "Y": "直腸",
        "Z": "肝臟",
        "a": "胰臟"
      }
    },
    "6": {
      "name": "背部",
      "Sub": {}
    },
    "7": {
      "name": "下盤",
      "Sub": {
        "b": "臀部",
        "c": "生殖器"
      }
    },
    "8": {
      "name": "形容外型",
      "Sub": {}
    },
    "9": {
      "name": "形容心理",
      "Sub": {}
    },
    "0": {
      "name": "抽象",
      "Sub": {}
    },
    "A": {
      "name": "骨骼",
      "Sub": {}
    },
    "B": {
      "name": "肌肉",
      "Sub": {}
    },
    "C": {
      "name": "神經",
      "Sub": {}
    },
    "D": {
      "name": "經脈",
      "Sub": {}
    },
    "E": {
      "name": "皮膚",
      "Sub": {}
    }
  }
  
```
