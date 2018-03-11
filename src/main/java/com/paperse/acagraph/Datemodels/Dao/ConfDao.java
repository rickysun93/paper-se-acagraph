package com.paperse.acagraph.Datemodels.Dao;

import com.paperse.acagraph.Datemodels.domain.Conf;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * Created by sunhaoran on 2018/3/11.
 */
public interface ConfDao extends JpaRepository<Conf, String> {
    public Conf findByConfname(String cn);
}
