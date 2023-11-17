<script>

import {ref} from "vue";

export default {
    name: "carousel-component",
    setup() {
        return {
            step: ref(1),
            value_side: ref(64),
            value_batch: ref(64),
            value_thresh: ref(0.88),
            value_Sta: ref(0.95),
            value_offset: ref(1.0),
            value_box:ref(0),
            value_layers:ref(0),
            value_crop:ref(0),
            value_ratio:ref(0.3),
            value_factor:ref(1),
            options:[1,2,3],
            model_r:ref(null),
            model_g:ref(null),
            model_b:ref(null),
            rules:{
                inputRules:[
                    {pattern: /^[0-9]*$/,message: "只能输入正整数",trigger:blur}
                ]
            },
            inputValue:ref(1),
        }
    },
    methods:{
        ToInt_side(){
            this.value_side=Math.round(this.value_side)
        },
        ToInt_batch() {
            this.value_batch=Math.round(this.value_batch)
        },
        ToInt_layers(){
            this.value_layers=Math.round(this.value_layers)
        },
        ToInt_factor(){
            this.value_factor=Math.round(this.value_factor)
        }
    },
}

</script>

<template>
    <q-form id="form-1">
        <div class="q-pa-md">
            <q-stepper
                v-model="step"
                vertical
                color="primary"
                animated
            >
                <q-step
                    :name="1"
                    title="Select campaign settings"
                    icon="settings"
                    :done="step > 1"
                >
                    <div>
                        <b>RGB Index</b>
                        <div style="margin-top: 10px"></div>
                        <div>
<!--                        <label for="r-band" style="margin-left:15px">R:</label>-->
                        <q-select clearable filled style="width: 20%;margin-bottom: 30px" id="r-band" label="R-Band" :options="options" v-model="model_r"></q-select>
<!--                        <label for="g-band" style="display: inline-block">G:</label>-->
                        <q-select clearable filled style="width: 20%;margin-bottom: 30px" id="g-band" label="G-Band" :options="options" v-model="model_g"></q-select>
<!--                        <label for="b-band" style="display: inline-block">B:</label>-->
                        <q-select clearable filled style="width: 20%;margin-bottom: 30px" id="b-band" label="B-Band" :options="options" v-model="model_b"></q-select>
                        </div>
                    </div>
                    <div style="margin-top: 30px">
                        <b>Points per Side</b>
                        <div class="q-pa-md">
                            <q-input
                                v-model.number="value_side"
                                type="number"
                                min="1"
                                filled
                                style="max-width: 200px"
                                @blur="ToInt_side"
                            />
                        </div>
                    </div>
                    <div style="margin-top: 30px">
                        <b>Points per Batch</b>
                        <div class="q-pa-md">
                            <q-form :rules="rules.inputRules">
                            <q-input
                                v-model.number="value_batch"
                                type="number"
                                min="1"
                                filled
                                style="max-width: 200px"
                                @blur="ToInt_batch"
                            />
                            </q-form>
                        </div>
                    </div>
                    <q-stepper-navigation>
                        <q-btn @click="step = 2" color="primary" label="Continue"/>
                    </q-stepper-navigation>
                </q-step>

                <q-step
                    :name="2"
                    title="Create an ad group"
                    caption="Optional"
                    icon="create_new_folder"
                    :done="step > 2"
                >
                    <div style="margin-top: 30px">
                        <b>Pred Iou Thresh</b>
                        <div class="q-pa-md">
                            <q-slider
                                v-model="value_thresh"
                                :min="0"
                                :max="1"
                                :step="0.002"
                                label
                                label-always
                                color="light-blue"
                            />
                        </div>
                    </div>
                    <div style="margin-top: 30px">
                        <b>Stability Score Thresh</b>
                        <div class="q-pa-md">
                            <q-slider
                                v-model="value_Sta"
                                :min="0"
                                :max="1"
                                :step="0.002"
                                label
                                label-always
                                color="pink"
                            />
                        </div>
                    </div>
                    <div style="margin-top: 30px">
                        <b>Stability_Score_Offset</b>
                        <div class="q-pa-md">
                            <q-slider
                                v-model="value_offset"
                                :min="0"
                                :max="1"
                                :step="0.002"
                                label
                                label-always
                                color="pink"
                            />
                        </div>
                    </div>
                    <q-stepper-navigation>
                        <q-btn @click="step = 3" color="primary" label="Continue"/>
                        <q-btn flat @click="step = 1" color="primary" label="Back" class="q-ml-sm"/>
                    </q-stepper-navigation>
                </q-step>

                <q-step
                    :name="3"
                    title="Ad template"
                    icon="assignment"
                    :done="step > 3"
                >
                    <div style="margin-top: 30px">
                        <b>Box_Nms_Thresh</b>
                        <div class="q-pa-md">
                            <q-slider
                                v-model="value_box"
                                :min="0"
                                :max="1"
                                :step="0.002"
                                label
                                label-always
                                color="pink"
                            />
                        </div>
                    </div>
                    <div style="margin-top: 30px">
                        <b>Crop_N_Layers</b>
                        <div class="q-pa-md">
                            <q-input
                                v-model.number="value_layers"
                                type="number"
                                min="0"
                                filled
                                style="max-width: 200px"
                                @blur="ToInt_layers"
                            />
                        </div>
                    </div>
                    <div style="margin-top: 30px">
                        <b>Crops_Nms_Thresh</b>
                        <div class="q-pa-md">
                            <q-slider
                                v-model="value_crop"
                                :min="0"
                                :max="1"
                                :step="0.002"
                                label
                                label-always
                                color="pink"
                            />
                        </div>
                    </div>
                    <div style="margin-top: 30px">
                        <b>Crop_Overlap_Ratio</b>
                        <div class="q-pa-md">
                            <q-slider
                                v-model="value_ratio"
                                :min="0"
                                :max="1"
                                :step="0.002"
                                label
                                label-always
                                color="pink"
                            />
                        </div>
                    </div>
                    <div style="margin-top: 30px">
                        <b>Crop_N_Points_Downscale_Factor</b>
                        <div class="q-pa-md">
                            <q-input
                                v-model.number="value_factor"
                                type="number"
                                min="0"
                                filled
                                style="max-width: 200px"
                                @blur="ToInt_factor"
                            />
                        </div>
                    </div>
                    <q-stepper-navigation>
                        <q-btn @click="step = 4" color="primary" label="Continue"/>
                        <q-btn flat @click="step = 2" color="primary" label="Back" class="q-ml-sm"/>
                    </q-stepper-navigation>
                </q-step>

                <q-step
                    :name="4"
                    title="Create an ad"
                    icon="add_comment"
                >
                    Try out different ad text to see what brings in the most customers, and learn how to
                    enhance your ads using features like ad extensions. If you run into any problems with
                    your ads, find out how to tell if they're running and how to resolve approval issues.

                    <q-stepper-navigation>
                        <q-btn color="primary" label="Finish"/>
                        <q-btn flat @click="step = 3" color="primary" label="Back" class="q-ml-sm"/>
                    </q-stepper-navigation>
                </q-step>
            </q-stepper>
        </div>
    </q-form>
</template>

<style scoped>
.q-pa-md {
//height: 500px;
}
</style>
