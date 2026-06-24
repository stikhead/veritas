import mongoose from "mongoose";

import crypto from "node:crypto"


const visitorSchema = mongoose.Schema({
    ipHash: {
        type: String,
        required: true,
        unique: true,
        index: true
    },

    country: {
        type: String
    },

    city: {
        type: String
    },

    attemptsToday: {
        type: Number,
        default: 0
    },

    lastAttemptAt: {
        type: Date,
        default: Date.now
    },

    expiresAt: {
        type: Date,
        index: { expires: 0 }
    }
}, {timestamps: true})

export const Visitor = mongoose.model('Visitor', visitorSchema)