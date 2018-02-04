## 数据models说明
1. tblUser
    1. id 用户id，作为识别用户的代码
    2. name 用户名
    3. password_hash 密码的hash值
    4. role_id 用户角色id
    5. money 用户金币数量
    6. photo 用户头像
    7. openid 微信登录识别id  
    实例方法
    1. tblUser.password 用于设置密码
    2. tblUser.verify_password(password) 验证密码

2. tblRole 角色权限管理
    1. id 角色id
    2. name 角色名称
    3. default 默认角色
    4. permissions 具有的权限
    5. users 与tblUser的关系，对应角色的所有用户

3. Room 游戏房间
    1. id 房间id
    2. createtime 房间创建时间
    3. confirm 进入房间后确认的字段，所有用户确认后，才可开始。达到2**room.count()-1表示全部确认
    4. user1_id 等 ，1-5号玩家的用户id
    5. end 表示房间游戏结束的字段，默认为0
    6. pajus 与Paiju的关系，该房间的所有牌局  
    > 待补充，房间及游戏状态信息
    > 房间：总局数，玩家信息，玩家状态，状态（当前局数，0；未开始，20：结束）
    > 牌局信息：玩家状态（准备，抢庄，下注，亮牌），庄，下注，
    实例方法
    1. room.userpos(user) 返回指定用户的座位号
    2. room.count() 返回房间玩家人数

4. Paiju 牌局
    1. id 牌局id
    2. room_id 所属房间id
    3. createtime 生成时间
    4. ready 所有玩家是否已准备，和是否已抢庄
    5. zhuang 判断玩家是否参与抢庄，后保存玩家位置，1、2、4、8、16
    6. done 玩家亮牌，本局结束
    7. finish 所有玩家亮牌，本局结束
    8. user1_xiazhu 1-5 号玩家下注金额
    9. xiazhudone 判断是否全部下注，达到2**room.count()-1表示全部确认
    10. user1_mark 计算各玩家得分
---
## 接口
1. 用户登录后，登录用户作为判断身份的依据，current_user，保存在cookies中
2. 创建或加入房间后，房间号保存在session中