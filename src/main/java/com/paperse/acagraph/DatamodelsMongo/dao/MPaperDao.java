package com.paperse.acagraph.DatamodelsMongo.dao;

import com.paperse.acagraph.DatamodelsMongo.domain.MPaper;
import org.springframework.data.mongodb.repository.MongoRepository;

/**
 * Created by sunhaoran on 2018/3/12.
 */
public interface MPaperDao extends MongoRepository<MPaper, String> {
}
