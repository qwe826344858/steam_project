/******************************************/
/*   DatabaseName = Steam_Project   */
/*   TableName = t_steam_item_single_day_info   */
/******************************************/
CREATE TABLE `t_steam_item_single_day_info` (
  `fid` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `fitem_id` bigint(20) NOT NULL DEFAULT '0' COMMENT '商品主键id',
  `fcalc_day` bigint(20) NOT NULL DEFAULT '0' COMMENT '计算的日期',
  `fsell_online_count` bigint(20) NOT NULL DEFAULT '0' COMMENT '当前在售数量',
  `fprices` int(16) NOT NULL DEFAULT '0' COMMENT '价格 美分',
  `fcurrency` varchar(8) NOT NULL DEFAULT '' COMMENT '当前货币',
  `faddtime` bigint(20) NOT NULL COMMENT '加入时间',
  PRIMARY KEY (`fid`),
  KEY `idx_item_id_calc_day` (`fitem_id`,`fcalc_day`),
  KEY `idx_addtime` (`faddtime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='steam市场商品每日价格记录表'
;
