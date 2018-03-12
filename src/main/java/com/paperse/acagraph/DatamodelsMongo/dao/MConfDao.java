package com.paperse.acagraph.DatamodelsMongo.dao;

import com.paperse.acagraph.DatamodelsMongo.domain.MConf;
import org.springframework.data.mongodb.repository.MongoRepository;

/**
 * Created by sunhaoran on 2018/3/12.
 */
public interface MConfDao extends MongoRepository<MConf, String> {
    public MConf findByConfname(String cn);
}
