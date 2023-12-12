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
        mask_result_src:"",//分割后图像的地址
        bar:ref(false),
        completion:ref(false),
        download_license:ref(false)
      }
  },
    methods:{
        ToInt_side(){
            this.value_side=Math.round(this.value_side)//Math.round代表四舍五入
            if(this.value_side<0){
              this.value_side=64;
              alert("值不能小于0！")
            }
        },
        ToInt_batch() {
            this.value_batch=Math.round(this.value_batch)
            if(this.value_batch<0){
              this.value_batch=64;
              alert("值不能小于0！")
            }
        },
        ToInt_layers(){
            this.value_layers=Math.round(this.value_layers)
            if(this.value_layers<0){
              this.value_layers=0;
              alert("值不能小于0！")
            }
        },
        ToInt_factor(){
            this.value_factor=Math.round(this.value_factor)
            if(this.value_factor<0){
              this.value_factor=1;
              alert("值不能小于0！")
            }
        },
        ToInt_min_mask(){
            this.value_min_mask=Math.round(this.value_min_mask)
            if(this.value_min_mask<0){
              this.value_min_mask=100;
              alert("值不能小于0！")
            }
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
        const layer=new ImageLayer
        ({
          source:new Static({
            url: this.mask_result_src,//到时候替换成image_src
            projection: projection,
            imageExtent: extent,
          })
        })
        this.use_map.addLayer(layer)
            this.bar=false
            this.completion=true
            this.download_license = true
          })
          .catch(error=>{
            console.error(error)
          })
        this.bar=true
      },
      download_img()//下载分割后的图像
      {
        if(this.download_license == false)
        {
          alert("请得到遥感图像后再使用")
        }
        else {
          window.open("/download")
        }
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
                    title="Sampling parameters"
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
                    title="Filtering parameters"
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
                        <b>Stability Score Offset</b>
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
                    title="Model parameters"
                    icon="assignment"
                    :done="step > 3"
                >
                    <div style="margin-top: 30px">
                        <b>Box Nms Thresh</b>
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
                        <b>Crop N Layers</b>
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
                        <b>Crops Nms Thresh</b>
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
                        <b>Crop Overlap Ratio</b>
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
                        <b>Crop N Points Downscale Factor</b>
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
                            @blur="ToInt_min_mask"
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
                    title="Finish"
                    icon="add_comment"
                >
                  You have completed all the parameter settings, please confirm that the input is correct.
                  Click "Finish" to start the image splitting, or click "Back" to go back to check.

                    <q-stepper-navigation>
                        <q-btn color="primary" label="Finish" @click="add_pr" />
                        <q-btn flat @click="step = 3" color="primary" label="Back" class="q-ml-sm"/>
                    </q-stepper-navigation>
                </q-step>
            </q-stepper>
        </div>
    </q-form>
  <q-dialog v-model="bar" >
    <q-card id="bar_dialog">
      <label id="bar_label">图像分割可能需要加载一段时间....</label>
      <br>
      <q-circular-progress
        indeterminate
        size="90px"
        color="lime"
        class="q-ma-md"
        id="bar_progress"
      />
    </q-card>
  </q-dialog>
  <q-dialog v-model="completion">
    <q-card style="width: 300px">
      <q-card-section>
        <div class="text-h6">通知</div>
      </q-card-section>
      <q-card-section class="q-pt-none">
        遥感图像分割完毕
      </q-card-section>
      <q-card-actions align="right" class="bg-white text-teal">
        <q-btn flat label="OK" v-close-popup />
      </q-card-actions>
    </q-card>
  </q-dialog>
  <q-btn id="download" color="primary" label="点击此处下载处理结果" @click="download_img"></q-btn>
</template>

<style scoped>
.q-pa-md {
//height: 500px;
}
#bar_dialog{
  width: 500px;
  height: 200px;
}
#bar_label{
  font-size: 30px;
  font-family: 微软雅黑;
}
#bar_progress{
  bottom: -20px;
  left: 180px;
}
#download{
  position: absolute;
  top:690px;
  left:1144px;
}
</style>
