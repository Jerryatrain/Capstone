### 流程报告：计算 `est_iopv` 和 `PD`

以159920 QDII ETF为例，跟踪HSI指数

#### **1. 数据准备**
获取 HSI 指数和港币兑人民币汇率（HKDCNY）的分钟数据。将 HSI 指数转换为人民币计价，并筛选出交易时间（9:40 至 16:00）的数据。
注意HKDCNY很多时候没有9:30-9:40的数据，使用backward fill填充

#### **2. 计算 HSI 指数的分钟级收益率**
：  
$\text{return} = \frac{\text{close}}{\text{previou close}}-1$

#### **3. 准备每日净值（NAV）数据**
并将前一日的NAV作为次日的初始NAV，且设置初试时间点为每日 9:40。


#### **5. 动态更新分钟级净值（`est_iopv`）**
每分钟的HSI收益率estimate iopv:  

$\text{est\_iopv} = \text{pre\_unit\_nav} \times \text{index daily cumulative return} $

注意，这里每天的初始iopv并不等于前一天nav，而是前一天nav * HSI指数昨日收盘到今日开盘（16:00 - 9:40）的收益率
#### **6. 计算溢价率（`PD`）**
我计算了每分钟的溢价率，公式是：  
$
\text{PD} = \frac{\text{fair price} - \text{est\_iopv}}{\text{est\_iopv}}
$
溢价率的波动为：

$
\text{jump\_PD}  = \text{PD} - \text{MA\_30\_PD}
$

提取波动>=0.0005, 0.001, 0.0015并查看波动后1-15分钟ETF价格变化