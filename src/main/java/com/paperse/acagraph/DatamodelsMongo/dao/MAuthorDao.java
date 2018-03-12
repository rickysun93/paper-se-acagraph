package com.paperse.acagraph.DatamodelsMongo.dao;

import com.paperse.acagraph.DatamodelsMongo.domain.MAuthor;
import org.springframework.data.mongodb.repository.MongoRepository;

/**
 * Created by sunhaoran on 2018/3/12.
 */
public interface MAuthorDao extends MongoRepository<MAuthor, String> {
    public MAuthor findByNamelower(String nl);
}
