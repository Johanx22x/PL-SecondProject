<template>
    <el-container class="container-sm">
        <el-main>
            <el-row justify="center">
                <el-col :span="6" class="m-4">
                    <el-card shadow="hover">
                        <el-avatar :size="100" :src="johan_avatar" class="mx-auto d-block"></el-avatar>
                        <el-divider></el-divider>
                        <el-text>
                            <h3 class="text-center">Johan Rodriguez</h3>
                            <p class="text-center">@Johanx22x</p>
                            <p class="text-center">A Computer Science student
                            at Costa Rica Institute of Technology.
                            </p>
                            <!-- Contact -->
                            <el-row justify="center">
                                <el-col :span="6">
                                    <el-link href="https://github.com/Johanx22x" target="_blank">
                                        <el-avatar :size="30" src="https://logos-download.com/wp-content/uploads/2016/09/GitHub_logo.png"></el-avatar>
                                    </el-link>
                                </el-col>
                                <el-col :span="6">
                                    <el-link href="https://www.linkedin.com/in/johan-rodr%C3%ADguez-5a49a223a/" target="_blank">
                                        <el-avatar :size="30" src="https://cdn.iconscout.com/icon/free/png-256/linkedin-208-916919.png"></el-avatar>
                                    </el-link>
                                </el-col>
                            </el-row>
                        </el-text>
                    </el-card>
                </el-col>
                <el-col :span="6" class="m-4">
                    <el-card shadow="hover">
                        <el-avatar :size="100" :src="aaron_avatar" class="mx-auto d-block"></el-avatar>
                        <el-divider></el-divider>
                        <el-text>
                            <h3 class="text-center">Aaron Gonzalez</h3>
                            <p class="text-center">@zSnails</p>
                            <p class="text-center">A Computer Science student
                            at Costa Rica Institute of Technology.
                            </p>
                            <!-- Contact -->
                            <el-row justify="center">
                                <el-col :span="6">
                                    <el-link href="https://github.com/zSnails" target="_blank">
                                        <el-avatar :size="30" src="https://logos-download.com/wp-content/uploads/2016/09/GitHub_logo.png"></el-avatar>
                                    </el-link>
                                </el-col>
                                <el-col :span="6">
                                    <el-link href="https://twitter.com/zSnails" target="_blank">
                                        <el-avatar :size="30" src="https://im.rediff.com/news/2023/jul/24twitter.jpg"></el-avatar>
                                    </el-link>
                                </el-col>
                            </el-row>
                        </el-text>
                    </el-card>
                </el-col>
            </el-row>
        </el-main>
    </el-container>
</template>

<script lang="ts">
    import { reactive, toRefs, defineComponent } from 'vue';

    const state = reactive({
        johan_avatar: 'https://avatars.githubusercontent.com/u/101372687',
        aaron_avatar: 'https://avatars.githubusercontent.com/u/35583049',
    });

    const { johan_avatar, aaron_avatar } = toRefs(state);

    export default defineComponent({
        name: 'AboutView',
        setup() {
            return {
                johan_avatar,
                aaron_avatar,
            };
        },
    });
</script>
