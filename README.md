# IIS_log_analysis

本程序可以分析IIS的日志文件。逐行读取记录后，提取、汇总访问信息（主要以来访IP为依据）。
分析后，每个文件生成一个当日摘要，当日汇总，并将当日汇总记录追加入相应的汇总文件。
程序运行时将自动解析来访IP地址的来源区域，以供下一步人工分析使用。
程序参数：
-h 帮助信息
*  处理本目录下所有log文件
<file_name[,filename]> 逐次处理文件列表中的文件
没有参数将只处理倒数第二个日志文件（以方便用于定期任务）
