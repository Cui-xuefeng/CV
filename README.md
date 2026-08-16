# 少数民族服饰语义分割系统

> 基于 **SegFormer** 与 **UNet** 的深度学习语义分割平台，提供图片分割与实时视频流分割能力，前后端分离架构（Flask + Vue3）。

![项目封面](https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=semantic%20segmentation%20visualization%20of%20ethnic%20minority%20costumes%20in%20China%2C%20person%20wearing%20traditional%20clothing%2C%20pixel-level%20segmentation%20mask%20overlay%2C%20colorful%20class%20regions%2C%20deep%20learning%20computer%20vision%2C%20clean%20technical%20illustration&image_size=landscape_16_9)

## 项目简介

本项目面向**少数民族服饰**的像素级语义分割任务，整合了两种主流语义分割模型，并通过 Web 可视化界面进行交互。系统支持：

- **图片分割检测**：上传单张图片，输出分割可视化结果
- **实时视频流分割**：通过摄像头采集视频流（MJPEG），逐帧进行分割推理
- **多模型切换**：前端支持在 SegFormer 与 UNet 之间切换对比

## 核心特性

- 基于 Transformer 的 **SegFormer（MiT-B2）** 分割模型
- 基于 CNN 的 **UNet（ResNet50 主干）** 分割模型
- Flask 后端提供 RESTful API 与 MJPEG 视频流
- Vue3 + TypeScript + Vite 前端，支持登录鉴权与路由守卫
- 训练评估一体化（mIoU / mPA / Precision / Recall / 混淆矩阵）

## 技术栈

| 模块 | 技术 |
| :--- | :--- |
| 后端框架 | Flask、Flask-CORS、Flask-JWT-Extended |
| 深度学习 | PyTorch、torchvision、TensorBoard |
| 视频处理 | OpenCV、Pillow |
| 分割模型 | SegFormer（MiT-B2）、UNet（ResNet50/VGG） |
| 前端框架 | Vue3、TypeScript、Vite、Vue Router |
| 数据格式 | VOC 格式（JPEGImages / SegmentationClass） |

## 项目结构

```
CV/
├── backend/                        # 后端服务
│   ├── app.py                      # Flask 应用入口（端口 5001）
│   ├── config.py                   # 基础配置
│   ├── core/                       # 实时检测核心（线程、全局状态）
│   ├── routes/                     # API 路由蓝图
│   │   ├── detect.py               # SegFormer 图片检测
│   │   ├── detect_unet.py          # UNet 图片检测
│   │   ├── detect_real.py          # SegFormer 实时视频流
│   │   └── detect_real_unet.py     # UNet 实时视频流
│   ├── model/
│   │   ├── segformer/              # SegFormer 模型实现
│   │   │   ├── segformer.py        # 推理封装
│   │   │   ├── train.py            # 训练脚本
│   │   │   ├── predict.py          # 预测脚本
│   │   │   ├── get_miou.py         # mIoU 评估
│   │   │   ├── voc_annotation.py   # VOC 数据集划分
│   │   │   ├── nets/               # 网络结构
│   │   │   ├── utils/              # 工具函数
│   │   │   └── model_data/         # 权重存放目录
│   │   └── unet/                   # UNet 模型实现
│   │       ├── unet.py             # 推理封装
│   │       ├── nets/               # 网络结构
│   │       └── model_data/         # 权重存放目录
│   ├── static/                     # 静态资源（检测结果输出）
│   └── utils/                      # 通用工具
└── web/                           # 前端应用
    ├── src/
    │   ├── views/                  # 页面（首页/图片检测/实时检测/登录）
    │   ├── components/             # Navbar、Footer
    │   ├── router/                 # 路由配置
    │   └── App.vue
    └── package.json
```

## 环境配置

### 后端

```bash
cd backend
pip install -r model/segformer/requirements.txt
# 额外依赖
pip install flask flask-cors flask-jwt-extended opencv-python pillow pandas
```

### 前端

```bash
cd web
npm install
```

## 模型权重下载

由于模型权重文件体积较大，未纳入仓库，请通过夸克网盘下载后放置到对应目录：

| 模型 | 下载地址 | 提取码 | 放置目录 |
| :--- | :--- | :--- | :--- |
| **SegFormer** | [夸克网盘](https://pan.quark.cn/s/c577f15cfede?pwd=dMcB) | `dMcB` | `backend/model/segformer/model_data/` |
| **UNet** | [夸克网盘](https://pan.quark.cn/s/1482801a87f0?pwd=CURM) | `CURM` | `backend/model/unet/model_data/` |

下载后将权重文件（`.pth`）放入上表对应目录，并按需修改推理脚本中的 `model_path` 路径。

## 快速开始

### 1. 启动后端

```bash
cd backend
python app.py
# 服务运行于 http://127.0.0.1:5001
```

### 2. 启动前端

```bash
cd web
npm run dev
# 默认开发服务器 http://localhost:5173
```

### 3. 使用

- 访问前端首页，登录后进入功能页面
- **图片检测**：选择模型（SegFormer / UNet）→ 上传图片 → 查看分割结果
- **实时检测**：开启摄像头 → 实时查看分割视频流

## API 接口

| 方法 | 路径 | 说明 |
| :--- | :--- | :--- |
| POST | `/local/img/detect` | SegFormer 图片分割检测 |
| POST | `/local/img/detect_unet` | UNet 图片分割检测 |
| POST | `/local/detect` | 启动实时视频流分割 |
| GET | `/local/video_feed` | MJPEG 视频流（`multipart/x-mixed-replace`） |

**图片检测请求示例：**

```json
{
  "mode": "predict",
  "image_base64": "data:image/jpeg;base64,/9j/4AAQ..."
}
```

## 分割类别

本项目针对少数民族服饰进行像素级语义分割，共定义 **9 个类别**（1 个背景 + 8 个服饰部件）：

| 索引 | 类别名 | 中文含义 |
| :---: | :--- | :--- |
| 0 | `_background_` | 背景 |
| 1 | `Headwear` | 头饰 |
| 2 | `hat` | 帽子 |
| 3 | `top` | 上衣 |
| 4 | `belt` | 腰带 |
| 5 | `pants` | 裤子 |
| 6 | `skirt` | 裙子 |
| 7 | `boots` | 靴子 |
| 8 | `necklace` | 项链 |

> 训练与评估时 `num_classes = 9`，对应上述类别数（含背景）。类别定义见 [get_miou.py](backend/model/segformer/get_miou.py)。

## 数据标注

数据集标签采用 **SAM3（Segment Anything Model 3）** 进行半自动分割标注：

1. 使用 SAM3 对原始少数民族服饰图像进行零样本分割，自动生成候选掩码
2. 人工校验与修正掩码边界，确保各服饰部件（头饰、上衣、腰带等）的分割精度
3. 将修正后的掩码转换为 VOC 格式标签图（`.png`，像素值 = 类别索引）
4. 通过 `json_to_dataset.py` 将标注结果转换为可直接训练的标签图

> 标签像素值规范：背景为 `0`，目标服饰部件按上表索引依次为 `1~8`。标注完成后使用 `voc_annotation.py` 划分训练集 / 验证集。

## 模型说明

### SegFormer

- **主干网络**：MiT-B2（Mix Transformer）
- **输入尺寸**：512 × 512
- **特点**：基于 Transformer 的语义分割模型，无需位置编码即可处理任意分辨率输入，兼具局部与全局注意力

### UNet

- **主干网络**：ResNet50（可选 VGG）
- **输入尺寸**：512 × 512
- **特点**：经典编码器-解码器结构，跳跃连接保留多尺度细节，适合纹理丰富的服饰分割

## 训练与评估

### 训练

数据集需组织为 VOC 格式：

```
VOCdevkit/
└── VOC2007/
    ├── JPEGImages/        # 原始图片（.jpg）
    ├── SegmentationClass/ # 标签（.png，像素值为类别索引）
    └── ImageSets/
        └── Segmentation/  # 训练/验证集 txt
```

```bash
cd backend/model/segformer
# 1. 生成训练集划分
python voc_annotation.py
# 2. 修改 train.py 中 num_classes、model_path、phi 等参数
# 3. 开始训练
python train.py
```

> 训练权重保存在 `logs/` 目录下，TensorBoard 日志同步记录 loss 与 mIoU 曲线。

### 评估 mIoU

```bash
cd backend/model/segformer
# 修改 get_miou.py 中 num_classes 与 name_classes
python get_miou.py
```

评估结果输出于 `miou_out/` 目录，包含：

- `detection-results/`：预测结果可视化
- `mIoU.png` / `mPA.png`：各类别指标曲线
- `Precision.png` / `Recall.png`：精确率与召回率曲线
- `confusion_matrix.csv`：混淆矩阵

## 配置参数

推理时可在各模型的 `segformer.py` / `unet.py` 中修改：

| 参数 | 说明 |
| :--- | :--- |
| `model_path` | 权重文件路径 |
| `num_classes` | 类别数（= 实际类别 + 1 背景） |
| `phi` | SegFormer 主干（b0~b5） |
| `backbone` | UNet 主干（resnet50 / vgg） |
| `input_shape` | 输入图片尺寸 |
| `mix_type` | 可视化方式（0 混合 / 1 仅分割图 / 2 去背景） |
| `cuda` | 是否使用 GPU |

## License

本项目代码遵循 MIT License，模型权重仅供学习研究使用。
