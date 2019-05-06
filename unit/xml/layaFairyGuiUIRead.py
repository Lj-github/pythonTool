#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/6 13:52
# @Author  : liujiang
# @File    : xmlRead.py
# @Software: PyCharm


from xml.etree.ElementTree import ElementTree, Element
import sys


def read_xml(in_path):
    '''读取并解析xml文件
      in_path: xml路径
      return: ElementTree'''
    tree = ElementTree()
    tree.parse(in_path)
    return tree


def write_xml(tree, out_path):
    '''将xml文件写出
      tree: xml树
      out_path: 写出路径'''
    tree.write(out_path, encoding="utf-8", xml_declaration=True)


def if_match(node, kv_map):
    '''判断某个节点是否包含所有传入参数属性
      node: 节点
      kv_map: 属性及属性值组成的map'''
    for key in kv_map:
        if node.get(key) != kv_map.get(key):
            return False
    return True


# ---------------search -----
def find_nodes(tree, path):
    '''查找某个路径匹配的所有节点
      tree: xml树
      path: 节点路径'''
    return tree.findall(path)


def get_node_by_keyvalue(nodelist, kv_map):
    '''根据属性及属性值定位符合的节点，返回节点
      nodelist: 节点列表
      kv_map: 匹配属性及属性值map'''
    result_nodes = []
    for node in nodelist:
        if if_match(node, kv_map):
            result_nodes.append(node)
    return result_nodes


# ---------------change -----
def change_node_properties(nodelist, kv_map, is_delete=False):
    '''修改/增加 /删除 节点的属性及属性值
      nodelist: 节点列表
      kv_map:属性及属性值map'''
    for node in nodelist:
        for key in kv_map:
            if is_delete:
                if key in node.attrib:
                    del node.attrib[key]
            else:
                node.set(key, kv_map.get(key))


def change_node_text(nodelist, text, is_add=False, is_delete=False):
    '''改变/增加/删除一个节点的文本
      nodelist:节点列表
      text : 更新后的文本'''
    for node in nodelist:
        if is_add:
            node.text += text
        elif is_delete:
            node.text = ""
        else:
            node.text = text


def create_node(tag, property_map, content):
    '''新造一个节点
      tag:节点标签
      property_map:属性及属性值map
      content: 节点闭合标签里的文本内容
      return 新节点'''
    element = Element(tag, property_map)
    element.text = content
    return element


def add_child_node(nodelist, element):
    '''给一个节点添加子节点
      nodelist: 节点列表
      element: 子节点'''
    for node in nodelist:
        node.append(element)


def del_node_by_tagkeyvalue(nodelist, tag, kv_map):
    '''同过属性及属性值定位一个节点，并删除之
      nodelist: 父节点列表
      tag:子节点标签
      kv_map: 属性及属性值列表'''
    for parent_node in nodelist:
        children = parent_node.getchildren()
        for child in children:
            if child.tag == tag and if_match(child, kv_map):
                parent_node.remove(child)


def getRootPosID(nodeList):
    for node in nodeList:
        if node.get("name") == 'rootPos':
            return node.get("id")


import os

if __name__ == '__main__':

    fairyGuiXmlFile = sys.argv[1]
    if not fairyGuiXmlFile:
        print("没有文件传入")
        exit(0)
    fp, fn = os.path.split(fairyGuiXmlFile)
    ft = fn.split(".")[1]
    print("fileType:" + ft)
    if ft != "xml":
        print("只支持 xml 格式文件")
        exit(0)

    tree = read_xml(fairyGuiXmlFile)
    nodes = find_nodes(tree, "displayList/")
    rootPos = getRootPosID(nodes)  # "n0_bebg"  # 关联的节点 取里面id  应该写死 不动
    if not rootPos:
        print("获取 rootPos  id 失败 请添加 name rootPos")
        exit(0)
    addTar = "relation"
    # laya 里面 应该是 只用一层 就能满足需求吧
    # 关联 位置内容 <relation target="n0_bebg" sidePair="right-left,bottom-top"/>
    # rootbg 关联  <relation sidePair="center-center,middle-middle" target="" />
    relation = create_node(addTar, {"target": rootPos, "sidePair": "right-left,bottom-top"}, '')
    for node in nodes:
        # 判断有没有.
        if node.get("id") == rootPos and len(find_nodes(node, addTar)) == 0:
            relationRoot = create_node(addTar, {"target": "", "sidePair": "center-center,middle-middle"}, '')
            node.append(relationRoot)
            continue
        if len(find_nodes(node, addTar)) == 0 and node.get("id") != rootPos:
            print(node.get("id"))
            node.append(relation)
    write_xml(tree, fairyGuiXmlFile)
