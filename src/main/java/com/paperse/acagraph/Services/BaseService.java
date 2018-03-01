package com.paperse.acagraph.Services;

import com.paperse.acagraph.Datemodels.Dao.AuthorDao;
import com.paperse.acagraph.Datemodels.Dao.PaperDao;
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
    protected PaperDao paperDao;

    @Autowired
    protected AuthorDao authorDao;

    protected static final Logger logger = LogManager.getLogger(BaseService.class);
}
