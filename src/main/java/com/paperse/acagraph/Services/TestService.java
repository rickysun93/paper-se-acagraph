package com.paperse.acagraph.Services;

import com.google.gson.Gson;
import com.paperse.acagraph.Datemodels.Readin.*;
import com.paperse.acagraph.Datemodels.domain.Author;
import com.paperse.acagraph.Datemodels.domain.Conf;
import com.paperse.acagraph.Datemodels.domain.Paper;
import com.paperse.acagraph.Utils.Constrain;
import org.springframework.stereotype.Service;

import java.io.*;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by sunhaoran on 2017/7/24.
 */
@Service
public class TestService extends BaseService{

//    @Transactional
//    public UserModifyDTO Modify(UserModifyParameter userModifyParameter){
//        Paper tangoUser = tangoUserDao.findByIdAndValid(userModifyParameter.getId(), true);
//        if(tangoUser == null){
//            logger.info("该用户不存在");
//            return new UserModifyDTO(1);
//        }
//        Boolean flag = tangoUser.getAddress().equals(userModifyParameter.getAddress());
//        tangoUser.setInfo(userModifyParameter);
//        tangoUserDao.save(tangoUser);
//        if(!flag){
//            RefreshDistance(tangoUser);
//        }
//        return new UserModifyDTO(0);
//    }

//    @Transactional
    public String Readin(){
        Gson gson = new Gson();
        String infilePath = Constrain.infilePath;

        String outfilePath = Constrain.outfilePath;

        // 正则表达式规则
        String regEx = "\\?id=[^&]+&";
        // 编译正则表达式
        Pattern pattern = Pattern.compile(regEx);

        try {
            //String encoding="GBK";
            File file = new File(infilePath);
            if(file.isFile() && file.exists()){ //判断文件是否存在
                InputStreamReader read = new InputStreamReader(new FileInputStream(file));//考虑到编码格式
                BufferedReader bufferedReader = new BufferedReader(read);
                String lineTxt = null;
                int i = 0;
                while((lineTxt = bufferedReader.readLine()) != null){
                    paperinfo pi = gson.fromJson(lineTxt, paperinfo.class);

                    Matcher matcher = pattern.matcher(pi.getPdfUrl());
                    if (matcher.find()){
                        String temp = matcher.group(0);
                        pi.setPaperid(temp.substring(4, temp.length()-1));
                    }

                    ArrayList<String> citationsid = new ArrayList<String>();
                    for(citation c : pi.getCitations()){
                        matcher = pattern.matcher(c.getUrl());
                        if(matcher.find()) {
                            String temp = matcher.group(0);
                            citationsid.add(temp.substring(4, temp.length() - 1));
                        }
                    }
                    pi.setCitationsid(citationsid);

                    ArrayList<String> referenceid = new ArrayList<String>();
                    for(reference c : pi.getReferences()){
                        matcher = pattern.matcher(c.getUrl());
                        if(matcher.find()) {
                            String temp = matcher.group(0);
                            referenceid.add(temp.substring(4, temp.length() - 1));
                        }
                    }
                    pi.setReferencesid(referenceid);

                    ArrayList<Integer> authorsid = new ArrayList<Integer>();
                    for(author c : pi.getAuthors()){
                        matcher = pattern.matcher(c.getUrl());
                        if(matcher.find()) {
                            String temp = matcher.group(0);
                            String oriid = temp.substring(4, temp.length() - 1);
                            Author oau = authorDao.findByNamelower(oriid);
                            if(oau != null){
                                authorsid.add(oau.getId());
                            } else {
                                Author au = new Author();
                                au.setName(c.getName());
                                au.setNamelower(oriid);
                                au.setOrg(c.getUrl());
                                Author nau = authorDao.saveAndFlush(au);
                                authorsid.add(nau.getId());
                            }
                        }
                    }
                    pi.setAuthorsid(authorsid);

                    confinfo c = pi.getConf_info();
                    Conf oconf = confDao.findByConfname(c.getConfname());
                    if(oconf != null){
                        pi.getConf_info().setCcid(oconf.getId());
                    }else{
                        Conf conf = new Conf();
                        conf.setName(c.getName());
                        conf.setTitle(c.getTitle());
                        conf.setConfname(c.getConfname());
                        conf.setHref(c.getHref());
                        conf.setConfurl(c.getConfurl());
                        Conf nconf = confDao.saveAndFlush(conf);
                        pi.getConf_info().setCcid(nconf.getId());
                    }

                    try{
                        OutputStream out = new FileOutputStream(outfilePath, true);
                        out.write((gson.toJson(pi)+'\n').getBytes());
                        out.close();
                    }catch(Exception e){
                        e.printStackTrace();
                    }

                    Paper paper = new Paper();
                    paper.setOriid(pi.getPaperid());
                    paper.setTitle(pi.getName());
                    paper.setAuthors("");
                    paper.setVuene(pi.getSession());
                    paper.setYear(pi.getConf_info().getCcid());
                    paper.setKeywords("");
                    paper.setFos("");
                    paper.setNcite(pi.getCitationsid().size());
                    paper.setRefs(gson.toJson(pi.getReferencesid()));
                    paper.setDoctype("");
                    paper.setPublisher("");
                    paper.setIsbn("");
                    paper.setPdf(pi.getPdfUrl());
                    paper.setUrl(pi.getUrl());
                    paper.setAbs(pi.getAbs());
                    paper.setAuthorsid(gson.toJson(pi.getAuthorsid()));
                    paperDao.save(paper);

                    if(i%100==0)
                        System.out.print(i+" ");
                    i++;
                }
                read.close();
            }else{
                System.out.println("找不到指定的文件");
            }
        } catch (Exception e) {
            System.out.println("读取文件内容出错");
            e.printStackTrace();
            return "{\"result\":\"error\"}";
        }
        return "{\"result\":\"OK\"}";
    }
}
