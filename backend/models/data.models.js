import mongoose from "mongoose";

const dataSchema = mongoose.Schema(
  {
    feedback: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "Feedback",
    },

    owner: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "User",
      index: true
    },

    input: {
      type: String,
      required: true,
      trim: true,
    },

    prediction: {
      label: {
        type: String,
        required: true,
      },
      confidence: {
        type: Number,
        required: true,
      },
    },

    relevancy: {
      relevant: {
        type: Boolean,
      },

      topSimilarity: {
        type: Number,
      },

      avgSimilarity: {
        type: Number,
      },

      labelCounts: {
        type: Map,
        of: Number,
      },
      matches: [
        {
          score: {
            type: Number,
          },
          label: {
            type: String,
          },
          text: {
            type: String,
          },
        },
      ],
    },
    explanation: {
      type: String,
      required: true,
      trim: true,
    },

    model: {
      type: String,
      enum: ["spam", "emotion"],
      required: true,
      index: true
    },
  },
  { timestamps: true },
);

export const Data = mongoose.model("Data", dataSchema);
