# 电子商务网站

- #### 环境

  - python3.9
  - postgresql14

- #### 框架

  - 前端Bootstrap
  - 后端flask

- #### 安装与运行

  - 安装依赖库

    ``` python
    pip install -r requirements.txt	
    ```

  - 运行程序

    ``` python
    python3 app.py
    ```

- #### 项目说明

  - 普通用户
    - 用户注册、登录、注销
    - 浏览商品，将商品加入和移除购物车
    - 购买商品后填写邮箱，向客户发送通知
    - 可以查看历史订单
  - 管理员
    - 管理员可以对商品进行修改、添加、删除
    - 管理员可以查看用户订单与销售情况
  - 文件说明
    - templates文件夹是项目所需的html文件
    - static中存放商品图片
    - app.py是程序入口，定义了各种网页的路由
    - 其他py文件提供了程序的类与接口

- #### 作者

  - 姓名：韩希贤
  - 学号：201930341045
  - 2021网络应用开发实验

  