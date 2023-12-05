<script>

import {ref} from "vue";

import {Projection} from "ol/proj";
import ImageLayer from "ol/layer/Image";
import Static from "ol/source/ImageStatic";

export default {
    name: "carousel-component",
    props:["use_map"],
    setup()
    {
        return {
            step: ref(1),
            value_side: ref(64),//Points per Side
            value_batch: ref(64),//Points per Batch
            value_thresh: ref(0.88),//Pred Iou Thresh
            value_Sta: ref(0.95),//Stability Score Thresh
            value_offset: ref(1.0),//Stability_Score_Offset
            value_box:ref(0),//Box_Nms_Thresh
            value_layers:ref(0),//Crop_N_Layers
            value_crop:ref(0),//Crops_Nms_Thresh
            value_ratio:ref(0.3),//Crop_Overlap_Ratio
            value_factor:ref(1),//Crop_N_Points_Downscale_Factor
            value_min_mask:ref(100),
            options:[1,2,3],
            model_r:ref(null),//R
            model_g:ref(null),//G
            model_b:ref(null),//B
            rules:{
                inputRules:[
                    {pattern: /^[0-9]*$/,message: "只能输入正整数",trigger:blur}
                ]
            },
            inputValue:ref(1),
        }
    },

  data(){
      return{
        mask_result_src:""//分割后图像的地址
      }
  },
    methods:{
      child_f(){
        alert(this.use_map)
      },
        ToInt_side(){
            this.value_side=Math.round(this.value_side)//Math.round代表四舍五入
        },
        ToInt_batch() {
            this.value_batch=Math.round(this.value_batch)
        },
        ToInt_layers(){
            this.value_layers=Math.round(this.value_layers)
        },
        ToInt_factor(){
            this.value_factor=Math.round(this.value_factor)
        },
      add_pr(){//参数设置完毕后，进行图像分割
          // this.$emit('fatherMethod');//子控件调用父控件,
        const formData=new FormData();
        const json_obj = {
          'out_raster':"result_out.tif",
          'rgb_index':this.options,
          'points_per_side':this.value_side,
          'points_per_batch':this.value_batch,
          'pred_iou_thresh':this.value_thresh,
          'stability_score_thresh':this.value_Sta,
          'stability_score_offset':this.value_offset,
          'box_nms_thresh':this.value_box,
          'crop_n_layers':this.value_layers,
          'crop_nms_thresh':this.value_crop,
          'crop_overlap_ratio':this.value_ratio,
          'crop_n_points_downscale_factor':this.value_factor,
          'min_mask_region_area':this.value_min_mask
        }
        console.log(json_obj)
        console.log(JSON.stringify(json_obj))
        alert("Hello World!")
        fetch('/segment', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(json_obj),
          credentials: 'include',
        }).then(
          status=>{
            fetch('/preview_mask',{
              method:'GET'
            })
                   const cookies=document.cookie.split(";")
      const cookieObj={}
      for (let i = 0; i < cookies.length; i++)
      {
        const cookie = cookies[i].trim();
        const [key, value] = cookie.split('=');
        cookieObj[key] = value;
      }
      this.mask_result_src="/front_end/cache/"+cookieObj['uuid']+"/"+"result_out.tif.mask.png"
        const extent = [100, 100, 500, 480];
        const projection = new Projection({
          code: 'xkcd-image',
          units: 'pixels',
          extent: extent,
        });
        const layer=new ImageLayer({
          source:new Static({
            url: this.mask_result_src,//到时候替换成image_src
            projection: projection,
            imageExtent: extent,
          })
        })
        this.use_map.addLayer(layer)
          }
        )
          .catch(error=>{
            console.error(error)
          })

      },
      download_img()//下载分割后的图像
      {
        fetch('/download',{
          method:'GET'
        })
      }
    },
}

</script>

<template>
<!--  <div><q-btn @click="download_img">点击此处下载结果</q-btn></div>-->
<!--  <label>{{use_map}}</label>-->
<!--    <q-btn @click="child_f">测试子控件变量</q-btn>-->
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

                      <b>min_mask_region_area</b>
                      <div class="q-pa-md">
                        <q-form :rules="rules.inputRules">
                          <q-input
                            v-model.number="value_min_mask"
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
                        <q-btn color="primary" label="Finish" @click="add_pr" />
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
