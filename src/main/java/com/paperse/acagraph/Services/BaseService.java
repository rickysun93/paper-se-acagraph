package com.paperse.acagraph.Services;

import com.paperse.acagraph.Datemodels.Dao.TangoUserDao;
import com.tagooo.op.Datemodels.Dao.*;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * Created by sunhaoran on 2017/7/19.
 */
@Service
public class BaseService {
    @Autowired
    protected ThirdLabelDao thirdLabelDao;

    @Autowired
    protected ServiceLabelDao serviceLabelDao;

    @Autowired
    protected BasicLabelDao basicLabelDao;

    @Autowired
    protected TangoUserDao tangoUserDao;

    @Autowired
    protected TangoServiceDao tangoServiceDao;

    @Autowired
    protected Service2PictureDao service2PictureDao;

    @Autowired
    protected UserStatsDao userStatsDao;

    @Autowired
    protected ServiceStatsDao serviceStatsDao;

    @Autowired
    protected User2ServiceDao user2ServiceDao;

    protected static final Logger logger = LogManager.getLogger(BaseService.class);
}
