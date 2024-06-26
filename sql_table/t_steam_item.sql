/******************************************/
/*   DatabaseName = Steam_Project   */
/*   TableName = t_steam_item   */
/******************************************/
CREATE TABLE `t_steam_item` (
  `fid` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `fitem_source_name` varchar(128) NOT NULL COMMENT '源名称',
  `fitem_cn_name` varchar(128) NOT NULL COMMENT '中文名称',
  `fsell_online_count` bigint(20) NOT NULL DEFAULT '0' COMMENT '当前在售数量',
  `fpic_url` varchar(256) NOT NULL DEFAULT '' COMMENT '图片url',
  `fshow_prices` varchar(256) NOT NULL DEFAULT '' COMMENT '展示价格',
  `fprices` int(16) NOT NULL DEFAULT '0' COMMENT '价格 美分',
  `fcurrency` varchar(8) NOT NULL DEFAULT '' COMMENT '当前货币',
  `faddtime` bigint(20) NOT NULL COMMENT '加入时间',
  `fmodifytime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`fid`),
  KEY `idx_item_source_name` (`fitem_source_name`),
  KEY `idx_item_cn_name` (`fitem_cn_name`),
  KEY `idx_modify_time` (`fmodifytime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='steam市场商品表'
;
