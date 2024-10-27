# 赌卡模拟器

这是一个使用PyQt5开发的赌卡模拟器游戏。模拟了NBA2KOL2中的赌卡行为，当然概率方面我做了一些暗改（手动狗头），因为我知道那个游戏大概率也是这样的。
游戏本身是开源的，是我在学习过程中的一个实验。该项目仅供交流探讨，因为一些图片的版权问题，请勿用于其他不正当用途。

![01](https://github.com/user-attachments/assets/217559e6-f716-49e8-b8ad-4787daf4e808)
![02](https://github.com/user-attachments/assets/769019f8-7f68-4ef3-90a7-c85131ea3e45)
![03](https://github.com/user-attachments/assets/fef65468-bf41-4053-bb43-c797cf1393ae)
![04](https://github.com/user-attachments/assets/91aa3df8-5a20-4790-a689-f64c0f96c205)



## 功能

- 模拟赌卡游戏
- 显示游戏结果和统计信息
- 提供多种背景和界面

## 游戏玩法

1. **开始游戏**：点击“开始游戏”按钮进入主界面。
2. **选择卡片等级**：使用滑块选择主卡和副卡的等级。
3. **合成卡片**：点击“合成”按钮尝试合成卡片。
4. **查看结果**：合成成功或失败后，查看结果并选择继续或结束游戏。

## 赌卡概率

- 当主卡和副卡等级相同时，合成成功率为50%。
- 当主卡和副卡等级不同时，成功率根据等级差异降低：
  - 等级差1：25%
  - 等级差2：15%
  - 等级差3：10%
  - 等级差4：5%
  - 等级差5：1%

## 称号系统

根据赌卡成功率，玩家可以解锁不同的称号：

- **黑脸大汉**：成功率低于20%
- **狗运不错**：成功率在20%到40%之间
- **天选之子**：成功率在40%到55%之间
- **寿元战士**：成功率在55%到70%之间
- **玩赖是吧？**：成功率高于70%

## 安装

1. 克隆此仓库：

   ```bash
   git clone https://github.com/yourusername/duka.git
   cd duka
   ```

2. 创建并激活虚拟环境：

   ```bash
   python -m venv venv
   source venv/bin/activate  # 对于Windows: venv\Scripts\activate
   ```

3. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

## 运行

在虚拟环境中运行以下命令启动应用程序：

python main.py
