package com.paperse.acagraph.Controllers;

import com.paperse.acagraph.Services.TestService;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Created by sunhaoran on 2017/7/19.
 */
public class BaseController {
    @Autowired
    protected TestService testService;

    protected static final Logger logger = LogManager.getLogger(BaseController.class);
}
