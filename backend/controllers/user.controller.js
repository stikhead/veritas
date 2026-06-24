import { User } from "../models/user.models.js";
import { ApiError } from "../utils/ApiError.js";
import { ApiResponse } from "../utils/ApiResponse.js";
import asyncHandler from "../utils/asyncHandler.js";
import jwt from "jsonwebtoken";
import axios from "axios";
import crypto from "node:crypto"
import dotenv from "dotenv/config"

const generateRefreshAndAccessToken = async (id) => {
    const user = await User.findById(id).select("+refreshToken")
    if (!user) {
        throw new ApiError(404, "User not found");
    }
    const refreshToken = await user.generateRefreshToken()
    const accessToken = await user.generateAccessToken()

    if(!refreshToken || !accessToken){
        console.log('some error occurred')
    }

    user.refreshToken = refreshToken
    await user.save({validateBeforeSave: true})
    return {refreshToken, accessToken}
}

const refreshAccessToken = asyncHandler(async(req, res)=>{
    
})
const googleAuth = asyncHandler( async (req, res)=>{
    const {code} = req.body;
    if(!code){
        throw new ApiError(400, "missing values");
    }

    const {data: tokens} = await axios.post(process.env.GOOGLE_OAUTH_URI, {
        client_id: process.env.GOOGLE_CLIENT_ID,
        client_secret: process.env.GOOGLE_CLIENT_SECRET,
        code: code,
        grant_type: 'authorization_code',
        redirect_uri: process.env.GOOGLE_REDIRECT_URI
    });

    const response = await axios.get(process.env.GOOGLE_VERIFICATION_URI, {
        headers: { Authorization: `Bearer ${tokens.access_token}`}
    })

    const {email, name} = response.data;
    const existingUser = await User.findOne({email}).select("+isVerified");
    if(existingUser){
        const {refreshToken, accessToken} = await generateRefreshAndAccessToken(existingUser._id);
        if(!existingUser.isVerified){
            existingUser.isVerified = true 
        }

        if(existingUser.verification){
            existingUser.verification.emailToken = undefined;
            existingUser.verification.emailTokenExpiry = undefined;
            existingUser.verification.passwordResetToken = undefined;
            existingUser.verification.passwordResetTokenExpiry = undefined;
            existingUser.verification.nextOtpAvailable = undefined;
        }

        await existingUser.save({validateBeforeSave: false})
        const safeUser = await User.findById(existingUser._id)
        return res
        .cookie('accessToken', `${accessToken}`, { 
            httpOnly: true,    
            secure: true,   
            sameSite: 'none',  
            path: '/',       
        })
        .cookie('refreshToken', `${refreshToken}`, { 
            httpOnly: true,    
            secure: true,   
            sameSite: 'none',  
            path: '/',       
        })
        .json(
            new ApiResponse(200, {safeUser, isNewUser: false}, "login success")
        )
    }
    
    const user = await User.create({
        email: email,
        userName: name,
        isVerified: true,
        password: crypto.randomBytes(32).toString('hex')
    })

    const {refreshToken, accessToken} = await generateRefreshAndAccessToken(user._id);
    const safeUser = await User.findById(user._id);
    
    return res
        .cookie('accessToken', `${accessToken}`, { 
            httpOnly: true,    
            secure: true,   
            sameSite: 'none',  
            path: '/',       
        })
        .cookie('refreshToken', `${refreshToken}`, { 
            httpOnly: true,    
            secure: true,   
            sameSite: 'none',  
            path: '/',       
        })
        .json(
            new ApiResponse(200, {safeUser, isNewUser: true}, "account created and logged in successfully")
        )
})