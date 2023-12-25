# langchain-example
使用Vicuna v1.3 33b gptq4的方式运行的大模型

## python3.11

## install

```bash
pip install -r requirements.txt
```

## 运行
    
```bash
python3.11 main.py
```

## 结果
效果不好

参考：[结果](./output.md)


## 建议
可以适当调整Vicuna的`repetition_penalty`参数值，推荐1到1.2之间调整。

有多个tool的时候，会影响大模型做决策，可以前面加上自然语言任务辅助大模型选择tool，
比如判断是罪名相关的内容，再使用大模型完成提取罪名，生成api接口参数的能力。

大模型解析内容，生成接口参数效果还是不错，但完成复杂任务效果不好。

建议使用openai，可以减少好多工作量。

或者本地大模型 + 一些自然语言任务辅助。

或者可以参考下Gorilla，好像fine-tune 调用API的能力到大模型里了



## 初始化git

```
git init

# 修改git的用户名称
git config user.name "showmecodett"

# rename branch
git branch -m main
```