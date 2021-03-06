#-*- coding: utf-8 -*-
import sys
import random
def shortestpath(graph,start,end,visited=[],distances={},predecessors={}):
    """Find the shortest path between start and end nodes in a graph"""
    # we've found our end node, now find the path to it, and return
    if start==end:
        path=[]
        while end != None:
            path.append(end)
            end=predecessors.get(end,None)
        return distances[start], path[::-1]
    # detect if it's the first time through, set current distance to zero
    if not visited: distances[start]=0
    # process neighbors as per algorithm, keep track of predecessors
    for neighbor in graph[start]:
        if neighbor not in visited:
            neighbordist = distances.get(neighbor,float("inf"))
            tentativedist = distances[start] + graph[start][neighbor]
            if tentativedist < neighbordist:
                distances[neighbor] = tentativedist
                predecessors[neighbor]=start
    # neighbors processed, now mark the current node as visited
    visited.append(start)
    # finds the closest unvisited node to the start
    unvisiteds = dict((k, distances.get(k,float("inf"))) for k in graph if k not in visited)
    closestnode = min(unvisiteds, key=unvisiteds.get)
    # now we can take the closest node and recurse, making it current
    return shortestpath(graph,closestnode,end,visited,distances,predecessors)

if __name__ == "__main__":
    # graph = {'a': {'w': 14, 'x': 7, 'y': 9},
    #         'b': {'w': 9, 'z': 6},
    #         'w': {'a': 14, 'b': 9, 'y': 2},
    #         'x': {'a': 7, 'y': 10, 'z': 15},
    #         'y': {'a': 9, 'w': 2, 'x': 10, 'z': 11},
    #         'z': {'b': 6, 'x': 15, 'y': 11}}

    graph = {'七里庙': {'五里墩': 1123, '十里铺': 1204},
 '三眼桥': {'唐家墩': 1478, '香港路': 1281},
 '三角湖': {'体育中心': 1454, '汉阳客运站': 1563},
 '三阳路': {'大智路': 1010, '黄浦路': 1155},
 '东亭站': {'岳家嘴': 928, '青鱼嘴': 1048},
 '东吴大道': {'五环大道': 1652},
 '东风公司': {'体育中心': 842, '沌阳大道': 1448, '车城东路': 2390},
 '中南路': {'宝通寺': 1417, '梅苑小区': 1095, '洪山广场': 966},
 '中山公园': {'循礼门': 1542, '青年路': 946},
 '丹水池': {'徐州新村': 1525, '新荣': 1437},
 '二七小路': {'兴业路': 1253, '罗家庄': 758},
 '二七路': {'头道街': 915, '徐州新村': 795},
 '云飞路': {'武汉商务区': 1227, '范湖': 884},
 '五环大道': {'东吴大道': 1652, '额头湾': 1655},
 '五里墩': {'七里庙': 1123, '汉阳火车站': 1012},
 '仁和路': {'园林路': 1332, '工业四路': 1634},
 '体育中心': {'三角湖': 1454, '东风公司': 842},
 '光谷广场': {'杨家湾': 1317},
 '六渡桥': {'汉正街': 850, '江汉路': 976},
 '兴业路': {'二七小路': 1253, '后湖大道': 1180},
 '利济北路': {'友谊路': 888, '崇仁路': 880},
 '前进村': {'国博中心北': 843, '建港': 1476},
 '十里铺': {'七里庙': 1204, '王家湾': 950},
 '友谊路': {'利济北路': 888, '循礼门': 986},
 '双墩': {'宗关': 982, '武汉商务区': 1824},
 '古田一路': {'古田二路': 1518, '舵落口': 1435},
 '古田三路': {'古田二路': 907, '古田四路': 795},
 '古田二路': {'古田一路': 1518, '古田三路': 907},
 '古田四路': {'古田三路': 795, '汉西一路': 820},
 '后湖大道': {'兴业路': 1180, '市民之家': 1667},
 '唐家墩': {'三眼桥': 1478, '石桥': 953},
 '四新大道': {'汉阳客运站': 928, '陶家岭': 1358},
 '园博园北': {'轻工大学': 2804, '金银湖': 2279},
 '园林路': {'仁和路': 1332, '罗家港': 1035},
 '国博中心北': {'前进村': 843, '国博中心南': 2110},
 '国博中心南': {'国博中心北': 2110, '老关村': 960},
 '堤角': {'新荣': 1165, '滕子岗': 1025},
 '复兴路': {'拦江路': 3277, '首义路': 718},
 '大智路': {'三阳路': 1010, '循礼门': 1082, '江汉路': 762, '苗栗路': 1856},
 '天河机场': {'航空总部': 6004},
 '太平洋': {'宗关': 1580, '硚口路': 1045},
 '头道街': {'二七路': 915, '黄浦路': 1202},
 '孟家铺': {'永安堂': 1478, '黄金口': 2761},
 '宋家岗': {'巨龙大道': 2039, '航空总部': 1426},
 '宏图大道': {'市民之家': 2422, '常青城': 2886, '盘龙城': 3945},
 '宗关': {'双墩': 982, '太平洋': 1580, '汉西一路': 920, '王家湾': 2531},
 '宝通寺': {'中南路': 1417, '街道口': 1238},
 '小龟山': {'洪山广场': 1168, '螃蟹岬': 929},
 '岳家嘴': {'东亭站': 928, '铁机路': 1032},
 '崇仁路': {'利济北路': 880, '硚口路': 1142},
 '工业四路': {'仁和路': 1634, '杨春湖': 1173},
 '巨龙大道': {'宋家岗': 2039, '盘龙城': 1643},
 '市民之家': {'后湖大道': 1667, '宏图大道': 2422},
 '常青城': {'宏图大道': 2886, '金银潭': 2012},
 '常青花园': {'杨汊湖': 756, '轻工大学': 1825, '金银潭': 1092, '长港路': 1725},
 '广埠屯': {'虎泉': 1612, '街道口': 951},
 '建港': {'前进村': 1476, '马鹦路': 953},
 '徐州新村': {'丹水池': 1525, '二七路': 795},
 '循礼门': {'中山公园': 1542, '友谊路': 986, '大智路': 1082, '江汉路': 896},
 '惠济二路': {'赵家条': 896, '香港路': 934},
 '拦江路': {'复兴路': 3277, '钟家村': 833},
 '新荣': {'丹水池': 1437, '堤角': 1165},
 '杨家湾': {'光谷广场': 1317, '虎泉': 1442},
 '杨春湖': {'工业四路': 1173, '武汉火车站': 809},
 '杨汊湖': {'常青花园': 756, '石桥': 1524},
 '梅苑小区': {'中南路': 1095, '武昌火车站': 900},
 '楚河汉街': {'洪山广场': 1077, '青鱼嘴': 1225},
 '武昌火车站': {'梅苑小区': 900, '首义路': 896},
 '武汉商务区': {'云飞路': 1227, '双墩': 1824},
 '武汉火车站': {'杨春湖': 809},
 '武胜路': {'汉正街': 1552, '琴台': 804},
 '永安堂': {'孟家铺': 1478, '玉龙路': 1243},
 '汉口北': {'滠口新城': 3410},
 '汉口火车站': {'范湖': 1216, '长港路': 1406},
 '汉正街': {'六渡桥': 850, '武胜路': 1552},
 '汉西一路': {'古田四路': 820, '宗关': 920},
 '汉阳客运站': {'三角湖': 1563, '四新大道': 928},
 '汉阳火车站': {'五里墩': 1012, '钟家村': 1573},
 '江城大道': {'老关村': 1201, '车城东路': 1748},
 '江汉路': {'六渡桥': 976, '大智路': 762, '循礼门': 896, '积玉桥': 3291},
 '沌阳大道': {'东风公司': 1448},
 '洪山广场': {'中南路': 966, '小龟山': 1168, '楚河汉街': 1077},
 '滕子岗': {'堤角': 1025, '滠口新城': 1120},
 '滠口新城': {'汉口北': 3410, '滕子岗': 1120},
 '玉龙路': {'永安堂': 1243, '王家湾': 900},
 '王家墩东': {'范湖': 1409, '青年路': 1002},
 '王家湾': {'十里铺': 950, '宗关': 2531, '玉龙路': 900, '龙阳村': 1107},
 '琴台': {'武胜路': 804, '钟家村': 864},
 '盘龙城': {'宏图大道': 3945, '巨龙大道': 1643},
 '石桥': {'唐家墩': 953, '杨汊湖': 1524},
 '硚口路': {'太平洋': 1045, '崇仁路': 1142},
 '积玉桥': {'江汉路': 3291, '螃蟹岬': 1579},
 '竹叶海': {'舵落口': 806, '额头湾': 943},
 '罗家庄': {'二七小路': 758, '赵家条': 882},
 '罗家港': {'园林路': 1035, '铁机路': 1170},
 '老关村': {'国博中心南': 960, '江城大道': 1201},
 '航空总部': {'天河机场': 6004, '宋家岗': 1426},
 '舵落口': {'古田一路': 1435, '竹叶海': 806},
 '苗栗路': {'大智路': 1856, '香港路': 932},
 '范湖': {'云飞路': 884, '汉口火车站': 1216, '王家墩东': 1409, '菱角湖': 1676},
 '菱角湖': {'范湖': 1676, '香港路': 931},
 '虎泉': {'广埠屯': 1612, '杨家湾': 1442},
 '螃蟹岬': {'小龟山': 929, '积玉桥': 1579},
 '街道口': {'宝通寺': 1238, '广埠屯': 951},
 '赵家条': {'惠济二路': 896, '罗家庄': 882},
 '车城东路': {'东风公司': 2390, '江城大道': 1748},
 '轻工大学': {'园博园北': 2804, '常青花园': 1825},
 '金银湖': {'园博园北': 2279, '金银湖公园': 1296},
 '金银湖公园': {'金银湖': 1296},
 '金银潭': {'常青城': 2012, '常青花园': 1092},
 '钟家村': {'拦江路': 833, '汉阳火车站': 1573, '琴台': 864, '马鹦路': 1024},
 '铁机路': {'岳家嘴': 1032, '罗家港': 1170},
 '长港路': {'常青花园': 1725, '汉口火车站': 1406},
 '陶家岭': {'四新大道': 1358, '龙阳村': 905},
 '青年路': {'中山公园': 946, '王家墩东': 1002},
 '青鱼嘴': {'东亭站': 1048, '楚河汉街': 1225},
 '额头湾': {'五环大道': 1655, '竹叶海': 943},
 '首义路': {'复兴路': 718, '武昌火车站': 896},
 '香港路': {'三眼桥': 1281, '惠济二路': 934, '苗栗路': 932, '菱角湖': 931},
 '马鹦路': {'建港': 953, '钟家村': 1024},
 '黄浦路': {'三阳路': 1155, '头道街': 1202},
 '黄金口': {'孟家铺': 2761},
 '龙阳村': {'王家湾': 1107, '陶家岭': 905}}
print (shortestpath(graph,'循礼门','洪山广场'))






