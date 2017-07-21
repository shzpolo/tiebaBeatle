import os
from queue import Queue
import requests
from bs4 import BeautifulSoup
import threading
import time
import pymysql
from pymysql.err import IntegrityError

host = '172.17.60.108'
user = 'hz'
passwd = 'hz123456'
db = 'test_hz'
state_add = r'C:\Users\Polo\PycharmProjects\test\ml_res\state'
info_add = r'C:\Users\Polo\PycharmProjects\test\ml_res\info_list'
sex_add = r'C:\Users\Polo\PycharmProjects\test\ml_res\sex_list'
#tieba_names = ['李毅', '', '', '橙光', '显卡']
tieba_names = ['bt', 'photoshop', 'psp', '电脑', '软件', '黑客', '手机', '病毒', 'ndsl', '显卡', '电脑故障', 'ps3', 'office2003', 'gba', 'vista', '杀毒', 'c语言','鹿晗', '吴亦凡', 
               '笔记本', 'msn', 'vb', '装机', 'nds', 'java', '网络', 'gif', 'e2', '硬件', '操作系统', 'cpu', 'c++', '虚拟光驱', '系统', '计算机', '网络知识', 'linux', 'xbox', 'xp', '邮箱',
               'matlab', 'amd', '网络技术', '图象制作', 'windows', '五笔', '电脑爱好者', '内存', '宽带', '超级搜霸', 'nvidia', 'ip', 'cad', 'gmail', 'realplayer', 'ppstream', '万能五笔',
               'uc', 'ati', '搜索', 'word', 'firefox', '超级解霸', '网络工程师', '红客', '刻录机', 'adsl', '搜索引擎', '音箱', '鼠标', 'dos', 'illustrator', '3dsmax', 'asp.net', 'it',
               'msnspace', 'c#', 'php', 'foobar', 'fireworks', '刻录', 'iis', 'pascal', '易语言', 'vf', 'dv', 'delphi', 'icq', '李宇春', '周笔畅', '韩寒', '张杰', '苏醒', '尚雯婕', '东方神起',
               'micky有天', '陈楚生', '许飞', '山下智久', '张靓颖', '胡灵', '韩庚', '俞灏明', '马天宇', '厉娜', '宋晓波', '王铮亮', '王栎鑫', '魏晨', '蔡依林', '周杰伦', '刘涛', '神话', '谢霆锋',
               'hero在中', '孙燕姿', 's.h.e', '刘力扬', '赤西仁', 'u-know允浩', '林俊杰', '姚政', '李俊基', '何洁', '吉杰', '吴尊', '龟梨和也', '张含韵', '明道', 'twins', '郝菲尔', '潘玮柏',
               '黄雅莉', 'rain', '刘德华', '赵雅芝', '刘亦菲', '萧亚轩', '张远', '刘洲成', '赵薇', '阿穆', '飞轮海', 'superjunior', '谭维维', '王啸坤', 'ella', 'reborn', '蔡妍', '王心凌',
               '张韶涵', '金希澈', '高娅媛', '师洋', '玄彬', '五月天', 'xiah俊秀', 'max昌珉', '林峰', '韩彩英', '吴建飞', '薛之谦', '林心如', '魏斌', '杨丞琳', '朱智勋', '林志颖', '俞思远',
               '罗志祥', '张晓晨', '黄晓明', '裴涩琪', '魏佳庆', '滨崎步', '陈晓旭', '张学友', '5566', '陈慧琳', '金正勋', 'w-inds', '林依晨', '炎亚纶', '郑元畅', '裴勇俊', '陈乔恩', '佘诗曼',
               'junjin', '贝克汉姆', '王力宏', '蒲巴甲', 'hot', '科比', '王绍伟', '郑秀文', '梁咏琪', '孙艺心', '钟欣桐', 'vitas', '言承旭', '权相宇', '张国荣', '陆虎', '韩国明星', '李先皓',
               '巫迪文', '张柏芝', '宋慧乔', '王菲', '黎姿', '蔡卓妍', '周渝民', '杨丹', '张亚飞', '任贤齐', '麦迪', '陈石', '陈怡川', '艾薇儿', '尹恩惠', '高磊', '全慧彬', 'beyond', '申彗星',
               '谢娜', '张佑赫', '宝儿', '陈冠希', '梁静茹', '张英兰', '张娜拉', '海鸣威', '亨利', '叶璇', '金莎', '布兰妮', '胡歌', '周华健', '安七炫', '因扎吉', '钟汉良', '纪敏佳', '容祖儿',
               '苏有朋', '郭彪', '宋承宪', '汤加丽', 'ss501', '崔始源', 'eric', '金基范', 'hebe', '唐禹哲', '陈泽宇', '罗纳尔多', '巩贺', '毛方圆', '芙蓉姐姐', '汪东城', '范冰冰', '张栋梁',
               '唐宁', '唐笑', '安以轩', '苏志燮', '柳云龙', '贺军翔', '向鼎', '李多海', '李曼', '李毅', '吴宗宪', '崔智友', '孙俪', '韩雪', '蔡思涛', '陈奕迅', '刘若英', '黄宗泽', '钟凯',
               '锦户亮', '李珉宇', '胡玫', '贾静雯', '刀郎', '小仓优子', '183club', '孙楠', '君君', '卡卡', '乔维怡', '韩佳人', '仓木麻衣', '郭富城', '古天乐', '舒畅', '花儿乐队', '章子怡',
               '艾梦萌', '金泰熙', '叶一茜', '董洁', '闫妮', '张力尹', '梁齐', '关8', 'battle', '吴卓羲', '熊汝霖', '邓丽君', '王欣如', '艾弗森', '安又琪', '黄家驹', '周星驰', '党宁', '朴正秀',
               '李孝利', '在熙', 'tony', '周路明', '姚思寅', '姜智焕', '陈坤', '泽尻绘里香', '欧文', '飞儿乐团', '张东健', '杨怡', '成宥利', '张惠妹', 'kinkikids', '林志玲', '黎明', '李贞贤',
               '金善雅', '姜东元', '易建联', '詹姆斯', '李东海', 'leah', '李玉刚', '扎西顿珠', '李东旭', '李连杰', '马雪阳', '金喜善', '高圆圆', '宣萱', '林爽', '朱雅琼', '王杰', '邓宁', '金钟民',
               '姚明', '迈克尔杰克逊', '孙协志', '全智贤', '梅艳芳', '泷泽秀明', '信乐团', '徐熙媛', '张信哲', '李茂', '郑伊健', '何润东', '东万', '陶喆', '周润发', '石田彰', '李玟', '后街男孩',
               '李湘', '金钟国', '周传雄', '沙溢', '亚由美', '徐若瑄', 'fany', '张智霖', '辰亦儒', '付静', '郑源', '华人明星', 'hyde', '千明勋', '邓超', '早安少女组', '蔡琳', '黄鑫', '张焱',
               '杨千桦', '吴克群', '古巨基', '木村拓哉', '吴奇隆', '李东健', 'news', 'zard', '金英云', 'selina', '许巍', '劳尔', '堂本光一', '金来元', '李丽珍', '胡彦斌', '金雅中', 'linkin',
               '许玮伦', '罗纳尔迪尼奥', 'eminem', 'arashi', '何炅', '纳什', '谭咏麟', '相叶弘树', '郭品超', '霍建华', '刘翔', '徐怀钰', '羽泉', '堀北真希', '林青霞', '赵仁成', '吴彦祖',
               '上田龙也', '梁朝伟', '姚晨', '郑丽媛', '陈晓东', '乔丹', '陈好', '安吉丽娜', '陈小春', '杨幂', '舒淇', '光良', '小小罗', '齐达内', '王艳', '六月', 'westlife', '李倩', '白冰',
               '李小龙', '成龙', '沈人杰', '费德勒', '后弦', '聂远', '中岛美嘉', 'manson', '希尔顿', '舒马赫', '周恩来', '宋祖英', '安室奈美惠', '内斯塔', '约翰尼德普', '朴信阳', '黄义达',
               '李成民', '内博贵', '游鸿明', '莱科宁', '李智楠', '蒋勤勤', '莎拉波娃', '张瑞希', '李英爱', '菅谷梨沙子', '吴斌', '松本润', '池城', '谢东', '阳蕾', 'energy', '陈浩民', '韩真真',
               '胡杏儿', '郑嘉颖', '霍思燕', '王仁甫', '于波', '李慧珍', '雅', '周慧敏', '山野', '徐静蕾', '吴建豪', '李克勤', '张一山', '郑靖文', '阿杜', '陆毅', '加内特', '焦恩俊', '长泽正美',
               '张赫', '那英', '倪虹洁', '杜淳', '佟大为', '陈绮贞', '李小璐', '杨俊毅', '舍甫琴科', '幸田来未', '南拳妈妈', '申正焕', '美国偶像', '蔡少芬', 'klose', '李赫在', '堂本刚', '卢洁云',
               '黄圣依', 'f4', 'keita', '小栗旬', '巩俐', 'se7en', '彬雨', 'wentworth', '钟嘉欣', '罗嘉良', '林秀晶', '天上智喜', '郭帅', '陈辰', '陈键锋', '林正英', '安在旭', '金贤重', 'tank',
               '元彬', '麦当娜', '黄海冰', '李莞', '李志勋', '张曼玉', '苏打绿', 'tim', '本乡奏多', '郑国霖', '杰拉德', '朱茵', 'christina', '韩智慧', '孟庭苇', '李在元', '赵鸿飞', '刘荷娜',
               '大冢爱', '朴树', '陈慧娴', '金城武', '布拉德皮特', '温峥嵘', '水木年华', 'mariah', '秦岚', '李恩珠', '户田惠梨香', '天仙mm', '尉迟琳嘉', '筱原凉子', '程显军', '杨乐乐', '孙悦',
               '卓依婷', '李嘉欣', '小s', '刘烨', '汪涵', '喻恩泰', '文根英', '沈晓海', '万绮雯', '王冰洋', '孙红雷', 'jake', '费玉清', '甄子丹', '邵仲衡', '李毅', '戒赌', '胥渡', '美剧',
               '火影忍者', '海贼王', '死神', '网球王子', '柯南', '死亡笔记', '犬夜叉', '圣斗士', '百变小樱', '虹猫蓝兔七侠传', '七龙珠', '卡卡西', '高达', '佐助', '大剑', '灌篮高手', '不二周助',
               '冢不二', '奥特曼', '我爱罗', '灰原哀', '彩云国物语', '动漫', '佐樱', '游戏王', '美少女战士', '杀生丸', '龙樱', '佐鸣', '爱丽丝学园', 'nana', '银魂', '越前龙马', '鸣人',
               '凉宫春日的忧郁', '鼬', '少年阴阳师', 'loli', '数码宝贝', '晓', '杀薇', 'fate', '手冢国光', '通灵王', 'sola', '变形金刚', '工藤新一', '流花', '网络美少女', '漫画', 'skip', '棋魂',
               '新兰', '樱兰高中美男部', '宠物小精灵', '不二越', '动画片', '机器猫', '幸运星', 'l', '地狱少女', '猫和老鼠', '动漫歌曲', '四驱兄弟', 'seed', '春野樱', '卡嘉莉', '风云', '小樱',
               '一骑当千', '旋风管家', '桔梗', 'eva', '流川枫', '毛利兰', '阿斯兰', '灼眼的夏娜', '基拉', '水果篮子', '蜡笔小新', '金色之弦', 'cosplay', 'kof', '凉风', '鼬樱', '仙流', '雏田',
               '零之使魔', '怪盗基德', '魔法少女奈叶', '嘻哈小天才', '圣少女', '迪达拉', '戈薇', '双部', '大蛇丸', '忍迹', '十二生肖守护神', '钢之炼金术师', '犬薇', '破面', '我的女神', '翼',
               '黑之契约者', '交响情人梦', '头文字d', '全职猎人', '米妙', 'air', '漫画图片', '夜神月', '杀戮都市', '幽游白书', '一露', '浪客剑心', '沙加', '伊藤润二', '迹不二', '天空之城',
               '立海大', '杀铃', '格雷少年', '女仆', '日番谷冬狮郎', '东京猫猫', '迹部', '神秘星球孪生公主', '冢熊', '风之圣痕', '光明之泪', '神兵玄奇', '撒加', '八神', '公主', '妖精的旋律',
               '忍者神龟', '我的野蛮王妃', 'saber', '今天开始做魔王', '宁次', '樱木花道', '钢铁三国志', '草莓100%', '最游记', '柯哀', '蔷薇少女', '遥远时空中', '菊丸英二', '濑户之花嫁', '猎人',
               '四圣兽', '全金属狂潮', '校园迷糊大王', '朽木白哉', '天是红河岸', '四代火影', '穆', '动感新势力', '日本漫画', '动画', '拉克丝', '雪见', '新兰永恒', '朽木露琪亚', '十二国记',
               'loveless', '卡通', '樱桃小丸子', '樱花大战', '宁天', '罗密欧与朱丽叶', '蝎', '唱k小鱼仙', '史上最强弟子兼一', '鸣雏', '鹿丸', '恐怖漫画', 'kanon', '我为歌狂', '足球小将',
               '保鲁夫拉姆', '不知火舞', '路飞', '人型电脑天使心', '秋蝉鸣泣之时', '鼬佐', '幽灵公主', '北斗神拳', '冰帝', '灵儿', '三井寿', '完美小姐进化论', '天上天下', '酷拉皮卡', '雅典娜',
               '驱魔少年', '真月谭月姬', '天使怪盗', '鼬鸣', '黑崎一护', '路比', '千与千寻', 'xxxholic', '动漫人物', '服部平次', '金田一', '新世纪福音战士', '魔女的考验', '凉宫春日', '网王舞台剧',
               '市丸银', '魔法咪路咪路', '杀桔', '龙葵', '不思议游戏', '龙狼传', '新条真由', '快兰', 'clamp', '圣魔之血', '双子星公主', '白露', '观月初', '火凤燎原', '重楼', '乱马', '妖精的尾巴',
               '霸王爱人', '沙穆', '吸血鬼骑士', '恋爱情结', '佐为', '声优', '天使禁猎区', '妹妹公主', 'x战记', '奇牙', '白恋', '舞-hime', '鬼眼狂刀', '小女神花铃', '神田', '闪灵二人组',
               '高达seed', '梦比优斯', '御姐', '棒球英豪', '龙崎', '宫崎骏', '卡妙', '星马烈', 'al王道', '霹雳赛车', '秦时明月', '李小狼', '索隆', '仙道彰', '月莲', '爱德华', '加菲猫',
               '我们的存在', '麦兜', '魔卡少女樱', '幸村精市', '加隆', '手鞠', '凤穴', '月如', '不二', '桃华月惮', '几米', '天天', '龙珠gt', '宁雏', '家庭教师hitmanreborn', '太空堡垒', '动漫帅哥',
               '动漫音乐', 'c.c.', '羽翼', '新手文', '草莓棉花糖', '藏马', '神乐', '宇宙骑士', '小霞', '绅士同盟', '米罗', '推理之绊', 'kl王道', '小遥', 'ac王道', '虚幻勇士', '忍足侑士',
               '英雄时代', '花流', 'clannad', '指尖奶茶', '封神演义', '武器种族传说', '绝爱', '安娜', '撒妙', '日本动漫', '蓝兰岛漂流记', '冲田总司', '尼亚', '白', '鹿鞠', '冢越', '奈落',
               '万有引力', 'all越王道', '法伊', '皮卡丘', '魔神坛斗士', '杀犬', '纯情房东俏房客', '蜂蜜与四叶草', '知世', '高桥凉介', '枢木朱雀', '虫师', '龙猫', '我樱', '塔矢亮', '神龙斗士',
               '阴阳师', '黑礁', '初音岛', '雪之少女', '新志', '克劳德', '花月', '快青', '景天', '法希', '琴酒', '真幸', '亚连', '日向枣', '恐怖宠物店', '星璇', '新撰组异闻录', '梅罗', '卡卡罗特',
               '中华小当家', '漫友', '传颂之物', '结界师', '光速跑者21号', '黑猫', '凌波丽', '贝吉塔', '圣母在上', '猫眼三姐妹', 'dn同人', 'keroro军曹', '秀逗魔导士', '南方公园', 'tf文',
               '井上织姬', '卡樱', '宁樱', '幸不二', '源辉二', '杀戮公主', '公主公主', '好大人', '热带雨林的爆笑生活', '剑风传奇', '樱兰高校', '虹猫', 'kyo', '火王', '百鬼夜行', '月', '鸣樱',
               '瑶玲啊瑶玲', '赤井秀一', '伊扎克', '不二樱', '李逍遥', '草摩由希', '山中井野', '攻壳机动队', '天元突破', '圣传', '纲手', '娜娜', 'shuffle', '长门有希', '魔神英雄坛', '飞轮少年',
               'tifa', '爱雏', '楼兰旖梦', '神风怪盗', '飞天小女警', '瞬', '真珠美人鱼', '蓝龙', '天使迷梦', '尼罗河的女儿', '葛力姆乔', '幸运四叶草', '寻找满月', '宇文拓', '恶灵猎人',
               '麻宫雅典娜', '光亮王道', '须王环', '精灵守护者', '甲贺忍法帖', '弗兰基一家', '迹越', '乌尔奇奥拉', '爱画漫画', '铃', '陀螺战士', '悟空', '动漫精品屋', '米老鼠', '神无月的巫女',
               '原创漫画', '城市猎人', '死神同人文', '天空战记', '君麻吕', '星马豪', '小魔女doremi', '乙女爱上姐姐', '筱原千绘', '黄金十四', '小智', '白一', '犬桔', '撒沙', '卡伊', '强殖装甲',
               '钢铁神兵', '精灵世纪', '布雷特', '狮子王',  '妮可罗宾', '安琪莉可', '鸟山明', '喜羊羊与灰太狼', '呛辣校园俏女生', '他和她的xxx',  '神谷薰', '惊爆草莓', '穆沙', '撒隆', '明日香',
               '高桥留美子', '爱须香草', '茈静兰', '史努比', '紫龙', '飞鸟', '奥林匹斯星传', 'is', '佐菲', '杀奈', '短篇漫画', '逮捕令', '哈尔的移动城堡','史黛拉', 'schooldays', '阿布', '孔拉德',
               '奥茨玛公主', '中国漫画', '欧美漫画', '海堂薰', '迪迦', '爱野美奈子', '小熊维尼', '兜', '盖亚', '撒布', '八神嘉儿', '宇宙刑警', '网王all樱', '飞段', '絮儿', '美美', '非主流',
               '减肥', '股票', '唯美', '时尚', '女人', '美容', '发型', '可爱', '汽车', '狗', '博客', '美食', '日记', '韩国流行时尚', '漂亮女人', '美食与烹饪', '单身贵族', '观赏鱼', '猫', '仓鼠',
               'sd娃娃', '化妆', '瘦身', '韩流服饰', '我的大学生活', '证券', '旅游', '身高', '有趣', '美白', '戒烟', '模特', '网友', '书法', '健康', '淑女', '女人世界', '女人乡', '烟', '宠物',
               '流行时尚', '畅所欲言', '哈士奇', '瘦脸', '乌龟', '日本流行时尚', '金鱼', '十字绣', '耳洞', '瘦腿', '娱乐时尚', '潮流', '藏獒', '旗袍', '宝石', '香水', '芭比', '足彩', '跑车',
               '巴西龟', '兔子', '素食', '煲汤', '热带鱼', '爱美', '古玩', '咖啡', '养生', '娃娃', '小资', '钓鱼', '车', '鹦鹉', '酒', '股票操盘手', '茶', '中国旅游', '饮食', '流行', '服装设计',
               '戒指', 'zippo', 'mm的糖果乐园', '萨摩耶', '吉娃娃', '端午节', '国画', '厨师', '圣诞节', '万智牌', '猫咪', '金毛', '荷兰猪', '金丝熊', '饮品', '书学', '葡萄酒', '龟', '豆花', 'ps',
               '北京', 'qq空间', '天津', '阳泉', 'ak', '别样春天', '个性签名', '石家庄', '上海', '芝麻茶馆', '明恩', '唐山', '中国城市', '米秀', '邹城', '索引越界', '庚吧美文区', '河北', '沈阳',
               '衡水', '沧州', '无聊', '绍恩', '颜贻跑', '成都', '南阳', '青岛', '泊头', '无锡', '哈尔滨', '浙江', '江苏', '重庆', '阳江', '大连', '符号', '保定', '宋明壮', '安丘', '呼和浩特',
               '山东', '绝小娃娃', '长春', '畅晨', '济南', '厦门', 'kimi', '太原', '河间', 'all尚', '深圳', '正定', '安平', '东光', '榆次', '武汉', '兖矿', '郑州', '山西', '洛阳', '贴吧', '2u',
               '西安', '大庆', '高平', '河南', '青州', '庚澈', '迁安', '郴州', '青县', '汉沽', '侯马', '深州', '塘沽', '蒙阴', '南京', '杨岗丽', '资料', '小光', '邯郸', '马海生', '小肉肉', '汉中',
               '修真', '四川', '广州', '苏州', '鹤岗', '广东', '滕州', '长治', '安徽', '飞雪', '东阿', '起点', '宁晋', '介休', '运城', '感人', '兖州', '夏津', '枣强', '费县', '冀州', '莱钢',
               '盐山', '齐齐哈尔', '盂县', '茌平', '东北', '大同', '定州', '济宁', '微山', '宗师贴图', '广西', '抚顺', '彬彬娱乐', '米花', '灌云', '个人照片', '凌源', '贵阳', '感人的故事',
               '秦皇岛', '汾阳', 'qq群', '乌鲁木齐', '荥阳', '高唐', '烟台', '平定', '天使', '嘉祥', '女人私房话', '湖南', '长沙', '平遥', '鞍山', '南宁', '靓之影音', '辽宁', '黑龙江', '黄岩',
               '廊坊', '依依桃子', '兰州', '男生', '曲阜', '太谷', '淮南', '羊羔组合', '咸阳', '宣武', '灵石', '祁县', '强特', '禹城', '集安', '海伦', '吉林市', '监利', '潍坊', '灌南', '南昌',
               '耀华', '小帆', '恶作剧狂想', '锦州', '晋城', '包头', '孟村', '杨杨', '临沂', '聊城', '风情楼', '女孩', '心然', '福州', '邢台', '连云港', '绍乔', '温州', '献县', '天宇拉面馆',
               '柳州', '德州', '襄樊', '我爱侃大山', '莘县', '东阳', '平山', '海兴', '湖北', '超级男声', '邓州', '肥城', '天津动漫', '推理', '张家口', '沭阳', '云浮', '嘉兴', '长三角', '开封',
               '涿州', '聊天', '蚌埠', '江西', '西城', '高密', '略阳', '定兴', '棒棒糖', '徐州', '高考', '鬼', '灵异', '河南大学', '大学', '汉服', '名字', '北京大学', '三国', '人大附中', '三校生',
               '十一学校', '中南大学', '清华大学', '空姐', '明朝', '四川大学', '天津师范大学', '河南工业大学', '考研', '171', '日本文化', '25中', '101', '天津财经大学', '专升本', '武汉大学',
               '老师', '北大附中', '心理', '中关村中学', '厦门大学', '南开中学', '石室中学', '北京电影学院', '首都师范大学', '新华中学', '南昌大学', '电子科技大学成都学院', '北京城市学院',
               '八一中学', '北京八中', '天津一中', '齐齐哈尔大学', '育英中学', '赵云', '中央民族大学', '青岛大学', '天津外国语学院', '诸葛亮', '山东师范大学', '西南交通大学', '铁一中', '龙',
               '曹操', '北师大实验中学', '控江中学', '天津七中', '护士', '黑龙江科技学院', '理工附中', '成都七中', '首师大附中', '武汉理工大学', '西城外国语学校', '实验中学', '十九中',
               '和平街一中', '上海金融学院', '清华附中', '燕山大学', '东直门中学', '怀柔一中', '湖北大学', '天津四中', '东南大学', '通辽五中', '山东经济学院', '通辽一中', '中北大学', '渤海大学',
               '长沙理工大学', '福州格致中学', '五十七中', '文化', '西安外国语大学', '中国传媒大学', '塘沽一中', '西南石油大学', '吉林大学', '武汉生物工程学院', '天津二中', '唐山一中',
               '北京农学院', '沈阳大学', '北方工业大学', '闽江学院', '山东理工大学', 'qq']
thread_nums = 10
anonymous_num = 0


class TiebaInfoBeatle():

    def __init__(self, name):
        self.com_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}
        self.folder_path=r'C:\tieba\info'
        self.tieba_url = 'https://tieba.baidu.com'
        self.tieba_name = name

    def request(self, url, header):
        try:
            res = requests.get(url, header)
            return res
        except Exception as e:
            print(e)
            return None

    def mkdir(self, path):
        path = path.strip()  # delete char at top and bottom, if (), delete nothing
        isExists = os.path.exists(path)
        if not isExists:
            print('Creating named"' + path + '" folder')
            os.makedirs(path)
            print('Complete!')
        else:
            print('Folder is exists!')

    def infoFind(self, a):
        ap = a.parent
        userA = None
        if ap is not None:
            user_line = ap.next_sibling
            if user_line is not None:
                span1 = user_line.find('span')
                if span1 is not None:
                    span2 = span1.find('span')
                    if span2 is not None:
                        userA = span2.find('a')
        if(userA == None):
            return None
        user_href = userA['href']
        user_url = self.tieba_url + user_href
        user_res = self.request(user_url, self.com_header)
        if user_res is None:
            return None
        span = BeautifulSoup(user_res.text, 'html.parser').find('span', class_='user_name')
        return span

    def ageFind(self, user_personal_span):
        span = user_personal_span
        if span is not None:
            userS = str(span)
            first_pos = userS.index('吧龄:') + 3
            second_pos = userS.find('年', first_pos)
            if second_pos != -1:
                age = float(userS[first_pos: second_pos])
            else:
                age = 0.0
            return age

    def nameFind(self, user_personal_span):
        span = user_personal_span
        if span is not None:
            userS = str(span)
            first_pos = userS.index('户名:') + 3
            second_pos = userS.find('<', first_pos)
            return userS[first_pos: second_pos]


    def postFind(self, user_personal_span):
        span = user_personal_span
        if span is not None:
            userS = str(span)
            #print(userS)
            first_pos = userS.find(r'发贴:') + 3
            second_pos = userS.find(r'万', first_pos)
            if second_pos == -1:
                second_pos = userS.find(r'<', first_pos)
                post = int(userS[first_pos: second_pos])
            else:
                post = int(float(userS[first_pos: second_pos]) * 10000)
            return post

    def sexFind(self, user_personal_span):
        div = user_personal_span.parent
        if div is not None:
            if div.find('span',{"class":"userinfo_sex userinfo_sex_male"}) is not None:
                #print('m')
                return 'male'
            else:
                #print('f')
                return 'female'

    def calc_page(self, soup):
        titles = soup.find('span', class_='red_text')
        if(titles == None):
            return 2
        mains = titles.text
        print(mains)
        try:
            mains = int(mains)
            mains /= 50
            return (mains - 1)
        except:
            return 10

    def get_title(self):

        print('Making directory folder')
        self.mkdir(self.folder_path)

        print('Change to target folder')
        os.chdir(self.folder_path)

        print('Getting connection with database.....')
        conn = pymysql.connect(host='172.17.60.108', user=user, password=passwd, db=db, charset='UTF8')
        cursor = conn.cursor()

        print('Requesting tieba of ' + self.tieba_name)
        total = 0
        sex_list = []
        info_list = []
        calculated_page = 5

        for page in range(calculated_page):
            tieba_header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
                'kw': self.tieba_name, 'ie': 'utf-8', 'pn': str(page * 50)}
            bar_url = self.tieba_url + '/f'
            res = self.request(bar_url, tieba_header)
            if res is None:
                continue
            soup = BeautifulSoup(res.text, 'html.parser')
            if soup.find('h2', class_='icon-attention'):
                break
            all_a = soup.find_all('a', class_='j_th_tit ')
            calculated_page = self.calc_page(soup)
            total += len(all_a)
            for a in all_a:
                if s.stop is False:
                    print('Thread engaging information of tieba of ' + self.tieba_name + ' is pausing.....')
                    time.sleep(5)
                    continue
                else:
                    span = self.infoFind(a)

                    if a is None:
                        continue

                    ag = self.ageFind(span)
                    po = self.postFind(span)
                    na = self.nameFind(span)
                    if ag and po and na is not None:
                        info_set = []
                        info_set.append(ag)
                        info_set.append(po)
                        info_list.append(info_set)
                        se = self.sexFind(a)
                        sex_list.append(se)
                        try:
                            cursor.execute("INSERT into test_hz.tieba_db (user_name, title, age, amount, sex) values ('{sql_user_name}', '{sql_title}', {sql_age}, {sql_amount}, '{sql_sex}');".format(sql_user_name=na, sql_title=a['title'], sql_age=ag,sql_amount=po, sql_sex=se))
                            conn.commit()
                        except IntegrityError as ie:
                            print('This user is duplicated, this information will not save again!')
                            conn.commit()
                            continue
                        except Exception as e:
                            print(
                                'There are some invalid character in the name or title. anonymous and no_title will added as name and title!')
                            cursor.execute("select val from state where state = 'An_id'")
                            anonymous_num = cursor.fetchone()[0]
                            cursor.execute(
                                "INSERT into test_hz.tieba_db (user_name, title, age, amount, sex) values ('{sql_user_name}', '{sql_title}', {sql_age}, {sql_amount}, '{sql_sex}');".format(
                                    sql_user_name='Anonymous' + str(anonymous_num), sql_title='no_title', sql_age=ag, sql_amount=po,
                                    sql_sex=se))
                            anonymous_num += 1
                            cursor.execute("update state set An_id = {new} where state = 'An_id'".format(new = anonymous_num))
                            conn.commit()
                            continue
                        #finally:
                            #cursor.close()
                            #conn.close()

                    print(a['title'])

        print(info_list)
        print(sex_list)
        cursor.close()
        conn.close()
        try:
            info_file_object = open(info_add, 'a')
            sex_file_object = open(sex_add, 'a')
            info_file_object.write(str(info_list))
            sex_file_object.write(str(sex_list))
            info_file_object.close()
            sex_file_object.close()
        except Exception as e:
            print(e)


class ThreadCrawl(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if name_queue is None or name_queue.empty() is True:
                break
            exe = TiebaInfoBeatle(name_queue.get())
            exe.get_title()


class ThreadState(threading.Thread):

    stop = True

    def __inti__(self):
        threading.Thread.__init__(self)

    def run(self):
        conn = pymysql.connect(host='172.17.60.108', user=user, password=passwd, db=db, charset='UTF8')
        cursor = conn.cursor()
        while True:
            f = open(state_add, 'r')
            state = f.read()
            row = cursor.execute("SELECT id from state where state = 'True';")
            #print('Prove I am alive, State is ' + str(row))
            if (state is not '1') or (row == 0):
                self.stop = False
            else:
                self.stop = True
            time.sleep(1)
            conn.commit()
            f.close()

# First send all tieba names which will construct url into queue
threads = []
name_queue = Queue()
for t_name in tieba_names:
    name_queue.put(t_name)


# Then open (n+1) threads, 1 for opration like pause and add, n for crawl
s = ThreadState()
s.setDaemon(True)
threads.append(s)
s.start()
time.sleep(1)
for thread_num in range(thread_nums):
    t = ThreadCrawl()
    threads.append(t)
    t.start()
    time.sleep(0.5)

for i in range(thread_nums + 1):
    threads[i].join()

