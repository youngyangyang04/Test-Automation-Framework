# Test-Automation-Framework

【代码随想录知识星球】项目分享-自动化测试框架

## 项目结构

```text

├── base                    # 基础工具类
├── common                  # 公共模块
├── conf                    # 配置文件
├── data                    # 测试数据
├── logs                    # 日志文件
├── report                  # 测试报告
│   ├── allureReport       # Allure报告
│   ├── temp               # 临时文件
│   └── tmreport           
├── testcase               # 测试用例
│   ├── Business interface # 业务流程测试
│   ├── ProductManager     # 商品管理测试
│   └── Single interface   # 单接口测试
├── conftest.py            # pytest配置文件
├── environment.xml        # 环境配置
└── run.py                 # 启动入口
```

## 使用说明

### 使用 “uv.lock” 安装依赖

```bash
uv sync
```

### 安装 allure

Mac 安装 allure

```bash
brew install allure
```

Windows 安装 allure

[text](https://allurereport.org/docs/install-for-windows/)

### 运行测试

```bash
uv run run.py
```
