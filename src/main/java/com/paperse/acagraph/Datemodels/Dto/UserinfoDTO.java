package com.paperse.acagraph.Datemodels.Dto;

import com.paperse.acagraph.Datemodels.domain.Paper;

/**
 * Created by sunhaoran on 2017/8/4.
 */
public class UserinfoDTO {
    private String id;
    //真实姓名
    private String name;
    //登录使用的用户名
    private String userName;
    //性别，0为女，1为男
    private boolean gender;
    //手机号码
    private String phone;
    //头像的路径
    private String photo;
    //上传头像次数
    private int photoNo;
    //自我描述
    private String description;
    //地理位置 经度
    private Double longitude;
    //地理位置 纬度
    private Double latitude;
    //地址
    private String address;
    //注册时间
    private String regDate;

    public String getRegDate() {
        return regDate;
    }

    public void setRegDate(String regDate) {
        this.regDate = regDate;
    }

    public UserinfoDTO(Paper tangoUser) {
        if(tangoUser != null) {
            this.setId(tangoUser.getId());
            this.setName(tangoUser.getName());
            this.setUserName(tangoUser.getUserName());
            this.setGender(tangoUser.isGender());
            this.setPhone(tangoUser.getPhone());
            this.setPhoto(tangoUser.getPhoto());
            this.setPhotoNo(tangoUser.getPhotoNo());
            this.setDescription(tangoUser.getDescription());
            this.setLongitude(tangoUser.getLongitude());
            this.setLatitude(tangoUser.getLatitude());
            this.setAddress(tangoUser.getAddress());
            this.setRegDate(tangoUser.getRegDate());
        }
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getUserName() {
        return userName;
    }

    public void setUserName(String userName) {
        this.userName = userName;
    }

    public boolean isGender() {
        return gender;
    }

    public void setGender(boolean gender) {
        this.gender = gender;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getPhoto() {
        return photo;
    }

    public void setPhoto(String photo) {
        this.photo = photo;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public int getPhotoNo() {
        return photoNo;
    }

    public void setPhotoNo(int photoNo) {
        this.photoNo = photoNo;
    }

    public Double getLongitude() {
        return longitude;
    }

    public void setLongitude(Double longitude) {
        this.longitude = longitude;
    }

    public Double getLatitude() {
        return latitude;
    }

    public void setLatitude(Double latitude) {
        this.latitude = latitude;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }
}
