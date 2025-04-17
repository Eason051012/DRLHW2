# HW2：使用價值迭代法推導最佳策略

---

## 📁 目錄架構
```bash
HW/
├── HW.py                # Flask 主程式（整合 HW1-1 與 HW1-2）
│
├── static/               # 靜態檔案（CSS、JS）
│   ├── styles.css        # 格子樣式與配色定義
│   └── script.js         # 使用者互動與資料傳送邏輯
│
├── templates/
│   └── index.html        # 主畫面（包含表單與動態網格）
│
└── README.md             # 專案說明檔
          
```
## 系統需求 
- Python 3.8 以上版本
- Flask 套件  

## 執行方式 
```bash
python HW.py
```
```cpp
http://127.0.0.1:5000/
```

## 方格設定說明（Grid Size）

   - 可輸入數字生成網格大小（範圍：5 ~ 9）
   - 預設為 5x5
   - 每次重新產生格子會清除之前設定

## 格子設定 (起點、終點、障礙物) 

   - 起點格（綠）第一次點擊格子。
   - 終點格（紅）第二次點擊格子。
   - 障礙格（灰）第三次起可繼續點擊（最多 n-2）。
   - 取消格子設定 → 再次點擊該格即可取消設定。
  
## 按鈕功能

   - 生成網格：依輸入數字建立新的 n × n 格子，並清除所有設定
   - 產生策略與價值：
   - 顯示 Policy Matrix（箭頭方向）與 Value Matrix（價值函數）   
   - 點擊 執行價值迭代（HW2） 按鈕後，系統會：
      使用 價值迭代演算法 更新每格 V(s)為每個合法格子指派「最佳行動方向」（↑↓←→）
      將從起點經由最佳策略走到終點的格子以黃色標記
